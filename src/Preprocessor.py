import ast
import re

from jsonpath_ng.parser import JsonPathParser
from mappingservice_plugincore.Preprocessor import Preprocessor as CorePreprocessor


class Preprocessor(CorePreprocessor):
    """
    JaMMaTo/MRI-specific preprocessing before schema construction.

    Generic datetime normalization comes from mappingservice_plugincore.
    This subclass keeps MRI/DICOM-specific behavior:
    - studyDate + studyTime -> studyDateTime
    - schema-specific unit normalization
    - stringified list conversion
    - program field schema compatibility
    """

    parser = JsonPathParser()

    unit_normalization = {
        "deg": "degree",
        "degr": "degree",
        "°": "degree",
        "\udcb0": "degree",
        "\udcb0C": "°C",
        "μm": "um",
        "µm": "um",
        "Secs": "s",
        "Mins": "min",
    }

    @classmethod
    def normalize_unit(cls, input_value) -> str:
        return cls.unit_normalization.get(input_value, input_value)

    @classmethod
    def normalize_all_units(cls, input_dict):
        unit_fields = cls.parser.parse("$..unit")
        unit_matches = [m for m in unit_fields.find(input_dict)]

        for m in unit_matches:
            if not isinstance(m.value, str):
                continue

            normalized_value = cls.normalize_unit(m.value)
            if normalized_value != m.value:
                m.full_path.update(input_dict, normalized_value)

    @classmethod
    def normalize_all_datetimes(cls, input_dict):
        # DICOM-specific combination: studyDate + studyTime -> studyDateTime
        if isinstance(input_dict, dict) and "studyDate" in input_dict and "studyTime" in input_dict:
            datetime_dict = {
                "Date": input_dict["studyDate"],
                "Time": input_dict["studyTime"],
            }
            input_dict["studyDateTime"] = cls.normalize_datetime(datetime_dict)

        # Generic datetime normalization inherited from plugincore behavior
        fields_for_normalization = ["creationTime", "startTime", "endTime"]
        for f in fields_for_normalization:
            date_fields = cls.parser.parse("$.." + f)
            date_matches = [m for m in date_fields.find(input_dict)]

            for m in date_matches:
                original_value = m.value
                normalized_value = cls.normalize_datetime(original_value)
                if normalized_value != original_value:
                    m.full_path.update(input_dict, normalized_value)

    @classmethod
    def normalize_string_lists(cls, input_dict):
        all_fields = cls.parser.parse("$..*")

        for match in all_fields.find(input_dict):
            original_value = match.value
            current_field = str(match.full_path)

            if "softwareVersions" in current_field:
                continue

            if not isinstance(original_value, str):
                continue

            if not (original_value.startswith("[") and original_value.endswith("]")):
                continue

            try:
                converted_value = ast.literal_eval(original_value)
                match.full_path.update(input_dict, converted_value)
            except (ValueError, SyntaxError):
                numbers = re.findall(r"-?\d+\.?\d*", original_value)
                if numbers:
                    converted_value = [
                        float(number) if "." in number else int(number)
                        for number in numbers
                    ]
                    match.full_path.update(input_dict, converted_value)

    @classmethod
    def normalize_program_field(cls, input_dict):
        program_fields = cls.parser.parse("$..program")

        for match in program_fields.find(input_dict):
            if isinstance(match.value, list):
                match.full_path.update(input_dict, str(match.value))