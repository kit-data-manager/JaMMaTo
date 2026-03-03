import logging
import numpy as np
from datetime import datetime, timezone
import re

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
            if not input_value.get("Date") and input_value.get("Time"): # Not possible to handle only Time
                logging.warning("Encountered complex date field, but cannot interpret it")
                return input_value
            if input_value.get("Date") and not input_value.get("Time"): # Handle only Date
                input_value["Time"] = "00:00:00"
                logging.info("Input with date information but no time information found. Setting time to 00:00:00")
            input_value = input_value.get("Date") + " " + input_value.get("Time")
        output_value = parse_datetime(input_value)
        if type(output_value) == datetime:
            if output_value.tzinfo:
                output_value = output_value.astimezone(timezone.utc) # datetime has timezone info, convert it to UTC
            else:
                output_value = output_value.replace(tzinfo=timezone.utc) # No timezone, assume it's already in UTC
            return output_value.isoformat().replace("+00:00", "Z")
        return input_value

    @staticmethod
    def normalize_all_datetimes(input_dict):
        # Handle studyDate + studyTime -> studyDateTime combination
        if isinstance(input_dict, dict) and 'studyDate' in input_dict and 'studyTime' in input_dict:
            # Create dict format that normalize_datetime expects
            datetime_dict = {
                "Date": input_dict['studyDate'],
                "Time": input_dict['studyTime']
            }
            combined_datetime = Preprocessor.normalize_datetime(datetime_dict)
            input_dict['studyDateTime'] = combined_datetime
        
        # Handle other datetime fields with original logic
        fields_for_normalization = ["creationTime", "startTime", "endTime"]
        for f in fields_for_normalization:
            date_fields = Preprocessor.parser.parse("$.." + f)
            date_matches = [m for m in date_fields.find(input_dict)]
            for m in date_matches:
                original_value = m.value
                normalized_value = Preprocessor.normalize_datetime(original_value)
                if normalized_value != original_value:
                    m.full_path.update(input_dict, normalized_value)

    @staticmethod
    def normalize_string_lists(input_dict):
        """
        Convert string representations of lists to actual lists.
        :param input_dict: dictionary to convert string lists in
        :return: None
        """
        
        all_fields = Preprocessor.parser.parse("$..*")
        
        for match in all_fields.find(input_dict):
            original_value = match.value
            current_field = str(match.full_path)
            
            if isinstance(original_value, str):
                # Convert string representations of lists to actual lists
                if original_value.startswith('[') and original_value.endswith(']'):
                    try:
                        converted_value = ast.literal_eval(original_value)
                        match.full_path.update(input_dict, converted_value)
                    except:
                        # Try to extract numbers from the string
                        numbers = re.findall(r'-?\d+\.?\d*', original_value)
                        if numbers:
                            converted_value = [float(n) if '.' in n else int(n) for n in numbers]
                            match.full_path.update(input_dict, converted_value)

    @staticmethod
    def normalize_program_field(input_dict):
        """
        Convert program field from list to string representation for schema compatibility.
        :param input_dict: dictionary to convert program field in
        :return: None
        """
        program_fields = Preprocessor.parser.parse("$..program")
        
        for match in program_fields.find(input_dict):
            if isinstance(match.value, list):
                converted_value = str(match.value)
                match.full_path.update(input_dict, converted_value)