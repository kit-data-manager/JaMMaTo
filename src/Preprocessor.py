import ast
import logging
from datetime import datetime

from jsonpath_ng.parser import JsonPathParser
from mappingservice_plugincore.Preprocessor import (
    Preprocessor as CorePreprocessor,
)


class Preprocessor(CorePreprocessor):
    """
    JaMMaTo/MRI-specific preprocessing before schema construction.

    Generic preprocessing behaviour comes from mappingservice_plugincore.
    This subclass keeps MRI/DICOM-specific behaviour:
    - studyDate + studyTime -> studyDateTime
    - smallest/largest image pixel value merging within one DICOM series
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
    def preprocess_series(cls, series_dict: dict) -> dict:
        """Apply historical JaMMaTo cleaning series by series."""
        for metadata_objects in series_dict.values():
            if not metadata_objects:
                continue

            cls.merge_date_time(
                metadata_objects,
                ["studyDate", "studyTime"],
                "studyDateTime",
            )
            cls.merge_min_max_values(
                metadata_objects,
                "smallestImagePixelValue",
                "largestImagePixelValue",
            )

        return series_dict

    @classmethod
    def merge_date_time(
        cls,
        metadata_objects: list,
        input_attributes: list,
        output_attribute: str,
    ) -> list:
        """Historical JaMMaTo Data_Cleaning.merge_date_time logic."""
        date_attribute, time_attribute = input_attributes

        for metadata in metadata_objects:
            if date_attribute not in metadata or time_attribute not in metadata:
                logging.warning(
                    "Skipping datetime merge: missing '%s' or '%s'.",
                    date_attribute,
                    time_attribute,
                )
                continue

            merged_date_time = (
                str(metadata[date_attribute]) + " " + str(metadata[time_attribute])
            )

            for date_format in ("%Y%m%d %H%M%S", "%Y%m%d %H%M%S.%f"):
                try:
                    merged_date_time = datetime.strptime(
                        merged_date_time,
                        date_format,
                    ).isoformat()
                    break
                except ValueError:
                    continue

            metadata.pop(date_attribute, None)
            metadata.pop(time_attribute, None)
            metadata[output_attribute] = merged_date_time

        return metadata_objects

    @classmethod
    def merge_min_max_values(
        cls,
        metadata_objects: list,
        min_attribute: str,
        max_attribute: str,
    ) -> list:
        """
        Merge the global minimum/maximum for DICOMs of one series.

        Smallest/Largest Image Pixel Value are optional DICOM attributes. If
        either one is missing in the series, this cleaning step is skipped and
        the mapping continues.
        """
        try:
            min_value = min(metadata[min_attribute] for metadata in metadata_objects)
            max_value = max(metadata[max_attribute] for metadata in metadata_objects)
        except (KeyError, TypeError, ValueError) as error:
            logging.warning(
                "Skipping merge_min_max_values because optional pixel range "
                "metadata is unavailable or invalid: %s",
                error,
            )
            return metadata_objects

        for metadata in metadata_objects:
            metadata[min_attribute] = min_value
            metadata[max_attribute] = max_value

        return metadata_objects

    @classmethod
    def transfer_to_list(cls, iterable_attribute) -> list:
        """Historical JaMMaTo Data_Cleaning.transfer_to_list logic."""
        new_list = []
        for value in iterable_attribute:
            if isinstance(value, (list, tuple)):
                new_list.append(cls.transfer_to_list(value))
            else:
                new_list.append(value)
        return new_list

    @classmethod
    def normalize_unit(cls, input_value) -> str:
        return cls.unit_normalization.get(input_value, input_value)

    @classmethod
    def normalize_all_units(cls, input_dict):
        unit_fields = cls.parser.parse("$..unit")
        for match in unit_fields.find(input_dict):
            if not isinstance(match.value, str):
                continue
            normalized_value = cls.normalize_unit(match.value)
            if normalized_value != match.value:
                match.full_path.update(input_dict, normalized_value)
        return input_dict

    @classmethod
    def normalize_all_datetimes(cls, input_dict):
        """
        Kept as MRI extension hook. Study date/time combination is performed
        before mapping by merge_date_time().
        """
        return input_dict

    @classmethod
    def normalize_string_lists(cls, input_dict):
        """Convert stringified Python lists into actual lists."""
        all_fields = cls.parser.parse("$..*")

        for match in all_fields.find(input_dict):
            if not isinstance(match.value, str):
                continue

            value = match.value.strip()
            if not (value.startswith("[") and value.endswith("]")):
                continue

            try:
                parsed_value = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                continue

            if isinstance(parsed_value, list):
                match.full_path.update(input_dict, parsed_value)

        return input_dict

    @classmethod
    def normalize_program_field(cls, input_dict):
        """
        MRI schema defines study.program as a string, while DICOM
        SoftwareVersions can be multi-valued. Preserve all values in one
        string, matching historical JaMMaTo output behaviour.
        """
        program_fields = cls.parser.parse("$..program")

        for match in program_fields.find(input_dict):
            if isinstance(match.value, (list, tuple)):
                match.full_path.update(input_dict, str(list(match.value)))

        return input_dict
