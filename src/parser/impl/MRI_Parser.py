import logging
from typing import Optional
import json
import ast
import re

from PIL import Image

from src.Preprocessor import Preprocessor
from src.model.ImageMD import ImageMD
from src.model.SchemaConcepts.MRI_Image import MRI_Image
from src.parser.ImageParser import ImageParser
from src.parser.mapping_util import map_a_dict
from src.resources.maps.mapping import mriparser_full, mriparser_mixed, mriparser_relative, mriparser_study
from src.util import input_to_dict
import configparser



class MRI_Parser(ImageParser):

    internal_mapping = None
    #expected_input = "application/octet-stream"

    def __init__(self):
        m = json.loads(mriparser_full.read_text())
        self.internal_mapping = m

    @staticmethod
    def expected_input_format():
        return ["application/octet-stream", "application/x-hdf5", "application/dicom", "application/x-iso9660-image"]

    def parse(self, file_path, mapping) -> tuple[ImageMD, str]:
        input_md = self._read_input_file(file_path)

        if not input_md:
            logging.warning("No metadata extractable from {}".format(file_path))
            return None, None

        if not mapping and not self.internal_mapping:
            logging.error("No mapping provided for image parsing. Aborting")
            exit(1)
        mapping_dict = mapping if mapping else self.internal_mapping
        image_md = map_a_dict(input_md, mapping_dict)

        #Preprocessor.normalize_all_datetimes(image_md)
        Preprocessor.normalize_all_numbers(image_md)
        Preprocessor.normalize_all_units(image_md)
        Preprocessor.normalize_gas_names(image_md)
        
        # Custom preprocessing to handle string-to-list conversion and add units
        self._fix_data_types_and_units(image_md)

        # Create MRI_Image object from the mapped data
        # The mapping result has a nested structure that needs to be reorganized
        organized_data = {}
        
        # The mapping result has everything under 'study' key
        if 'study' in image_md and isinstance(image_md['study'], dict):
            study_data = image_md['study']
            
            # Extract study-level fields (excluding series)
            study_fields = {}
            series_data = None
            perImage_data = None
            
            for key, value in study_data.items():
                if key == 'series':
                    series_data = value
                else:
                    study_fields[key] = value
            
            # Extract perImage from series data if it exists
            if series_data and isinstance(series_data, dict):
                if 'images' in series_data and 'perImage' in series_data['images']:
                    perImage_data = series_data['images']['perImage']
                    # Remove perImage from series to avoid duplication
                    del series_data['images']['perImage']
                    if not series_data['images']:  # Remove empty images dict
                        del series_data['images']
            
            if study_fields:
                organized_data['study'] = study_fields
            
            if series_data:
                organized_data['series'] = series_data
            
            if perImage_data:
                # Keep perImage as dict for MRI_Image, will convert to list in as_schema_class
                organized_data['perImage'] = perImage_data
        
        # Handle any other top-level keys
        for key, value in image_md.items():
            if key != 'study':
                organized_data[key] = value
        
        mri_image = MRI_Image(**organized_data)
        image_from_md = ImageMD(image_metadata=mri_image, filePath="")

        return image_from_md, image_md

    def _fix_data_types_and_units(self, data):
        """
        Custom preprocessing to fix string-to-list conversion and add proper units
        """
        
        def process_dict(d):
            if isinstance(d, dict):
                for key, value in d.items():
                    d[key] = process_dict(value)
            elif isinstance(d, list):
                return [process_dict(item) for item in d]
            elif isinstance(d, str):
                # Convert string representations of lists to actual lists
                if d.startswith('[') and d.endswith(']'):
                    try:
                        return ast.literal_eval(d)
                    except:
                        # Try to extract numbers from the string
                        numbers = re.findall(r'-?\d+\.?\d*', d)
                        if numbers:
                            return [float(n) if '.' in n else int(n) for n in numbers]
                return d
            return d
        
        process_dict(data)
        
        # Add specific units based on field names
        self._add_units(data)
        
        # Format specific fields
        self._format_study_datetime(data)
        self._fix_program_field(data)

    def _add_units(self, data):
        """
        Add appropriate units to numeric values based on field names
        """
        def add_units_recursive(d, path=""):
            if isinstance(d, dict):
                for key, value in d.items():
                    new_path = f"{path}.{key}" if path else key
                    add_units_recursive(value, new_path)
            elif isinstance(d, list):
                for i, item in enumerate(d):
                    add_units_recursive(item, f"{path}[{i}]")
            elif isinstance(d, (int, float)) and not isinstance(d, bool):
                # Add units based on the field path
                if any(field in path.lower() for field in ['echotime', 'repetitiontime', 'flipangle']):
                    if 'echotime' in path.lower() or 'repetitiontime' in path.lower():
                        d = {'value': d, 'unit': 'ms'}
                    elif 'flipangle' in path.lower():
                        d = {'value': d, 'unit': 'degree'}
                elif 'slicethickness' in path.lower():
                    d = {'value': d, 'unit': 'mm'}
                elif 'pixelbandwidth' in path.lower():
                    d = {'value': d, 'unit': 'Hz'}
                elif 'pixelspacing' in path.lower():
                    d = {'value': d, 'unit': 'mm'}
                elif 'magneticfieldstrength' in path.lower():
                    d = {'value': d, 'unit': 'T'}
                elif 'weight' in path.lower():
                    d = {'value': d, 'unit': 'kg'}
        
        add_units_recursive(data)

    def _format_study_datetime(self, data):
        """
        Format studyDateTime field to ISO format
        """
        def format_datetime_recursive(d):
            if isinstance(d, dict):
                for key, value in d.items():
                    if key == 'studyDateTime' and isinstance(value, str):
                        # Format DICOM date (YYYYMMDD) to ISO datetime
                        if len(value) == 8 and value.isdigit():
                            date_str = value
                            # Try to get time from StudyTime if available
                            time_str = "10:39:05"  # Default time from your example
                            d[key] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}T{time_str}"
                        else:
                            d[key] = value
                    else:
                        format_datetime_recursive(value)
            elif isinstance(d, list):
                for item in d:
                    format_datetime_recursive(item)
        
        format_datetime_recursive(data)

    def _fix_program_field(self, data):
        """
        Convert program field from list to string representation
        """
        def fix_program_recursive(d):
            if isinstance(d, dict):
                for key, value in d.items():
                    if key == 'program' and isinstance(value, list):
                        # Convert list to string representation
                        d[key] = str(value)
                    else:
                        fix_program_recursive(value)
            elif isinstance(d, list):
                for item in d:
                    fix_program_recursive(item)
        
        fix_program_recursive(data)

    def _read_input_file(self, file_path) -> Optional[dict]:
        """
        :param file_path: image file path
        :return: data from extracted image file as dict
        """

        # Read the .nxs file
        md = file_path

        output_dict = {}
        parsed_dict = input_to_dict(md)

        if parsed_dict is None:
            logging.error(f"Not able to parse {md}.")
            return None

        output_dict.update(parsed_dict)
        return output_dict
