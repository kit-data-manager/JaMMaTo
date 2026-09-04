import logging
import re
from typing import Hashable

from jsonpath_ng.ext.parser import ExtentedJsonPathParser

from src.IO.MappingAbortionError import MappingAbortionError


parser = ExtentedJsonPathParser()


def escape_pathelements(dotted_path) -> str:
    function = re.search(r"(`.+`)", dotted_path)
    if function:
        dotted_path = dotted_path.replace(function.group(0), "FUNCTIONPLACEHOLDER")

    escaped_elements = []
    for path_element in dotted_path.split("."):
        if not path_element:
            continue
        if "[" in path_element:
            to_escape, to_keep = path_element.split("[", 1)
            path_element = f"'{to_escape}'[{to_keep}"
        else:
            path_element = f"'{path_element}'"
        if path_element == "'FUNCTIONPLACEHOLDER'" and function:
            path_element = function.group(0)
        escaped_elements.append(path_element)
    return ".".join(escaped_elements)


def create_unified_dict(mapping, input_dict) -> dict:
    output_dict = {}

    for input_path, output_path in mapping.items():
        escaped_input_path = escape_pathelements(input_path)
        input_expression = parser.parse(escaped_input_path)
        output_expression = parser.parse(output_path)
        values = [match.value for match in input_expression.find(input_dict)]

        if not values:
            logging.warning(
                "Mapping defined but no corresponding value found in input dict: %s",
                escaped_input_path,
            )
            continue

        if "*" not in output_path:
            if all(isinstance(value, Hashable) for value in values):
                if len(set(values)) != 1:
                    raise MappingAbortionError(
                        "Mapping input to output format failed. Mapping not applicable."
                    )
            elif len(values) > 1:
                logging.warning(
                    "Found multiple complex values; only the first will be used."
                )

            if values[0]:
                output_expression.update_or_create(output_dict, values[0])
            else:
                logging.warning(
                    "Found a value equivalent to None. path: %s, value: %s",
                    escaped_input_path,
                    values[0],
                )
        else:
            for index, value in enumerate(values):
                if value:
                    parser.parse(output_path.replace("*", str(index))).update_or_create(
                        output_dict, value
                    )

    if not output_dict:
        logging.error(
            "No output was produced by applying map to input. "
            "Was the correct mapping used?"
        )
        raise MappingAbortionError(
            "Mapping input to output format failed. Mapping not applicable."
        )
    return output_dict


def map_a_dict(input_dict, mapping_dict) -> dict:
    return create_unified_dict(mapping_dict, input_dict)

__all__ = [
    "create_unified_dict",
    "escape_pathelements",
    "map_a_dict",
]
