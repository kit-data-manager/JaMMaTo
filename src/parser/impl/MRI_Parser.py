import logging
from typing import Optional
import json
import re

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
        
        Preprocessor.normalize_all_datetimes(input_md)
        
        image_md = map_a_dict(input_md, mapping_dict)

        Preprocessor.normalize_all_units(image_md)
        Preprocessor.normalize_string_lists(image_md)
        Preprocessor.normalize_program_field(image_md)

        # Create MRI_Image object from the mapped data
        # The mapping result has a nested structure that needs to be reorganized
        ac_md_format = {}
        
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
                ac_md_format['study'] = study_fields
            
            if series_data:
                ac_md_format['series'] = series_data
            
            if perImage_data:
                # Keep perImage as dict for MRI_Image, will convert to list in as_schema_class
                ac_md_format['perImage'] = perImage_data
        
        # Handle any other top-level keys
        for key, value in image_md.items():
            if key != 'study':
                ac_md_format[key] = value
        
        mri_image = MRI_Image(**ac_md_format)
        image_from_md = ImageMD(image_metadata=mri_image, filePath="")

        return image_from_md, image_md

    def _read_input_file(self, file_path) -> Optional[dict]:
        """
        :param file_path: image file path
        :return: data from extracted image file as dict
        """

        # Read the .nxs file
        md = file_path

        output_dict = {}
        parsed_dict = input_to_dict(md)
        print("+++++++  ",parsed_dict)

        if parsed_dict is None:
            logging.error(f"Not able to parse {md}.")
            return None

        output_dict.update(parsed_dict)
        return output_dict
