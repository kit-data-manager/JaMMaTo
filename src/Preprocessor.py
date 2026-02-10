import logging
import numpy as np
from datetime import datetime

from jsonpath_ng.parser import JsonPathParser

from src.model.SchemaConcepts.Schema_Concept import parse_datetime


class Preprocessor:
    """
    Use / adapt / extend for final preprocessing steps before converting a dictionary into the according pydantic class instances
    """

    parser = JsonPathParser()

    unit_normalization = {
        'deg': 'degrees',
        'degr': 'degrees',
        '°': 'degrees',
        '\udcb0': 'degrees',
        '\udcb0C': '°C',
        'μm': 'um',
        'Secs': 's',
        'Mins': 'min'
    }

    @staticmethod
    def get_expected_type(field_path):

        expected_types = {
            "entry.entry_identifier": "string_type",
            "entry.instrument.monochromator.grating.period.value": "int_type",
            "entry.sample.gas_flux[*].value": "float_type"
        }

        return expected_types.get(field_path, None)

    @staticmethod
    def normalize_unit(input_value) -> str:
        if input_value in Preprocessor.unit_normalization.keys():
            return Preprocessor.unit_normalization[input_value]
        return input_value

    @staticmethod
    def normalize_all_units(input_dict):
        """
        Inplace normalization of all values in fields "unit"
        :param input_dict: dictionary to replace units in
        :return: None
        """
        unit_fields = Preprocessor.parser.parse("$..unit")
        unit_matches = [m for m in unit_fields.find(input_dict)]
        for m in unit_matches:
            if type(m.value) != str: continue #TODO: should this be possible?
            original_value = m.value
            if not Preprocessor.unit_normalization.get(original_value): continue

            normalized_value = Preprocessor.unit_normalization[original_value]
            if normalized_value != original_value:
                m.full_path.update(input_dict, normalized_value)

    @staticmethod
    def normalize_datetime(input_value) -> str:
        if type(input_value) == dict:
            if not input_value.get("Date") and input_value.get("Time"):
                logging.warning("Encountered complex date field, but cannot interpret it")
                return input_value
            input_value = input_value.get("Date") + " " + input_value.get("Time")
        output_value = parse_datetime(input_value)
        if type(output_value) == datetime:
            return output_value.isoformat()
        return input_value

    @staticmethod
    def normalize_all_datetimes(input_dict):
        fields_for_normalization = ["creationTime", "startTime", "endTime"] #we could do it more generically but may want to limit it to specific fields

        for f in fields_for_normalization:
            date_fields = Preprocessor.parser.parse("$.." + f)
            date_matches = [m for m in date_fields.find(input_dict)]
            for m in date_matches:
                original_value = m.value
                normalized_value = Preprocessor.normalize_datetime(original_value)
                if normalized_value != original_value:
                    m.full_path.update(input_dict, normalized_value)

    @staticmethod
    def normalize_all_numbers(input_dict):
        """
        In-place conversion of numeric strings into integers or floats, but checks if it's an appropriate field.
        :param input_dict: dictionary to convert numeric values in
        :return: None
        """
        number_fields = Preprocessor.parser.parse("$..*")  # Traverse all fields

        for match in number_fields.find(input_dict):
            original_value = match.value
            current_field = str(match.full_path)
            expected_type = Preprocessor.get_expected_type(current_field)
            #print("<<<<>>>>  ",original_value)
                
            # Handle type conversions if needed (e.g.: int_type, float_type)
            if isinstance(original_value, str):
                try:
                    if expected_type == "int_type": # Convert only if it's a valid integer-like string
                        converted_value = int(original_value)
                        match.full_path.update(input_dict, converted_value)
                    elif expected_type == "float_type": # Convert only if it's a valid float-like string
                        converted_value = float(original_value)
                        match.full_path.update(input_dict, converted_value)
                except ValueError:
                    logging.warning(f"Error while trying to convert '{original_value}' into {expected_type} for field {current_field}")
                    continue
            
            # Check if the value is a numpy array
            if isinstance(original_value, np.ndarray) and original_value.size > 0:
                try:
                    converted_value = np.array([int(x) if isinstance(x, (int, str)) and not np.isnan(x) 
                                                else float(x) if isinstance(x, (float, str)) and not np.isnan(x) 
                                                else x 
                                                for x in original_value], dtype=float)

                    match.full_path.update(input_dict, converted_value)
                except ValueError:
                    logging.warning(f"Error while converting numpy array values for field {current_field}")
                    continue

    @staticmethod
    def normalize_gas_names(input_dict):
        gas_fields = Preprocessor.parser.parse("$..gas_name")

        for match in gas_fields.find(input_dict):
            original_value = match.value
            # Extract gas name if it's stored incorrectly (e.g., "/entry/sample/gas_flux_C2H4")
            if isinstance(original_value, str) and "/" in original_value:
                possible_gas = original_value.split("_")[-1]
                match.full_path.update(input_dict, possible_gas)
            else:
                logging.warning(f"Unexpected gas name format: {original_value}")

