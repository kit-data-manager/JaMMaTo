import logging
import re
import typing
import numpy as np
from jsonpath_ng.ext.parser import ExtentedJsonPathParser
from mappingservice_plugincore.exceptions.MappingAbortionError import MappingAbortionError
import re

parser = ExtentedJsonPathParser()

def escape_pathelements(dotted_path):
    funct_match = re.search(r"`(.+?)`", dotted_path)
    if funct_match:
        function_name = funct_match.group(1)
        if function_name == "arithmetic":
            return dotted_path.replace(f"`{function_name}`", "FUNCTIONPLACEHOLDER")

    path_elements = dotted_path.split(".")
    escaped_elements = []
    for pe in path_elements:
        if not pe: 
            continue
        if "[" in pe:
            to_escape, to_keep = pe.split("[", 1)
            escaped = f"'{to_escape}'"
            pe = escaped + "[" + to_keep
        else:
            pe = f"'{pe}'"
        if pe == "'FUNCTIONPLACEHOLDER'":
            pe = "`arithmetic`"
        escaped_elements.append(pe)
    return ".".join(escaped_elements)

def flatten_dict(d, parent_key="", sep="."):
    flattened = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict) and v:
            flattened.update(flatten_dict(v, new_key, sep))
        else:
            flattened[new_key] = v
    return flattened

def extract_base_path(path: str):
    match = re.match(r"^(.*)\.(\w+\[\-?\d+\])$", path)
    if match:
        base_path, sort_function = match.groups()
        return base_path, sort_function
    return path, None

def apply_arithmetic(myArray):
    minValue = np.nanmin(myArray)
    maxValue = np.nanmax(myArray)
    avgValue = (minValue + maxValue) / 2.
    
    arithmetic = [round(el, 3) if not np.isnan(el) else el for el in [minValue, maxValue, avgValue]]

    arithmetic_dict = {'min_value': arithmetic[0], 'max_value': arithmetic[1], 'avg_value': arithmetic[2]}
    return arithmetic_dict


def get_matching_keys(original_path_template,input_dict):
    # Check if the original_path_template contains (`*`)
    if '*' in original_path_template:
        # Extract the prefix like 'entry.sample.gas_flux_'
        prefix = original_path_template.split('*')[0]
        suffix = original_path_template.split('*')[-1]
        matching_keys = [k for k in flatten_dict(input_dict).keys() if k.startswith(prefix) and k.endswith(suffix)] # Find all keys in the original_dict that match the prefix
    else:
        matching_keys = [original_path_template]
    return matching_keys

def create_unified_dict(mapping, input_dict):
    output_dict = {}

    for k, v in mapping.items():
        escaped_v = escape_pathelements(v)
        v1, v2 = extract_base_path(escaped_v)

        # Handle ARITHMETIC paths
        if v2:
            index = 0 if '[0]' in v2 else -1 if '[-1]' in v2 else 1 if '[1]' in v2 else None
            exprIN = parser.parse(v1)
            exprOUT = parser.parse(k)
            values = [m.value for m in exprIN.find(input_dict)]

            try:
                if values and len(values[0]) > 0:
                    arithmetic_result = apply_arithmetic(values[0])
                    if index == 0:
                        result = arithmetic_result.get("avg_value")
                    elif index == -1:
                        result = arithmetic_result.get("min_value")
                    elif index == 1:
                        result = arithmetic_result.get("max_value")
                    else:
                        logging.warning("Unsupported index: {}, used in path: {}".format(index, v2))
                        continue

                    exprOUT.update_or_create(output_dict, result)
                else:
                    logging.warning("Found a value equivalent to None. path: {}, value: {}".format(v, values[0]))
            except Exception as e:
                logging.error("Unexpected error: {} at path: {}, values: {}".format(e, v, values))
            continue  # Skip rest since this path is handled

        # Handle (*) mapping
        if "*" in k:
            v_list = [escape_pathelements(el) for el in get_matching_keys(v, input_dict)]
            exprIN_list = [parser.parse(el) for el in v_list]
            values = []
            for exprIN in exprIN_list:
                val = [
                    m.value.item() if isinstance(m.value, np.ndarray) and len(m.value) == 1 else m.value
                    for m in exprIN.find(input_dict)
                ]
                values.extend(val)
        else:
            exprIN = parser.parse(escaped_v)
            exprOUT = parser.parse(k)
            values = [
                m.value.item() if isinstance(m.value, np.ndarray) and len(m.value) == 1 else m.value
                for m in exprIN.find(input_dict)
            ]

        if not values:
            logging.warning(f"Mapping defined but no corresponding value found in input dict: {v}")
            continue

        # Handle regular output
        if "*" not in k:
            try:
                if not all(isinstance(x, typing.Hashable) for x in values):
                    logging.warning("Found multiple complex values in input dict, but output target is not a list. Only the first value will be used.")
                else:
                    assert len(set(values)) == 1
            except AssertionError:
                logging.error(f"Found multiple values in input dict, but output target is not a list. Aborting. Input path: {v}, values: {values}")
                raise MappingAbortionError("Mapping input to output format failed. Mapping not applicable.")

            try:
                if len(values) > 0:
                    exprOUT.update_or_create(output_dict, values[0])
                else:
                    logging.warning("Found a value equivalent to None. path: {}, value: {}".format(v, values[0]))
            except Exception as e:
                logging.error("Unexpected error: {} at path: {}, values: {}".format(e, v, values))
        else:
            for i, value in enumerate(values):
                if value:
                    indexed_expr = parser.parse(k.replace('*', str(i)))
                    indexed_expr.update_or_create(output_dict, value)
                else:
                    logging.warning("Found a value equivalent to None. path: {}, value: {}".format(v, value))

    if not output_dict:
        logging.error("No output was produced by applying map to input. Was the correct mapping used?")
        raise MappingAbortionError("Mapping input to output format failed. Mapping not applicable.")

    logging.info(f"Successfully mapped {len(output_dict)} fields from input")
    return output_dict


def map_a_dict(input_dict, mapping_dict):
    return create_unified_dict(mapping_dict, input_dict)