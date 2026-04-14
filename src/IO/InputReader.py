import os
import logging
from typing import Dict, Any

from src.IO.MappingAbortionError import MappingAbortionError
from src.IO.MapfileReader import MapFileReader
from src.model.ImageMD import ImageMD
from src.model.SchemaConcepts.MRI_Image import MRI_Image
from src.parser.ParserFactory import ParserFactory
from src.parser.impl.MRI_Parser import MRI_Parser
from src.util import input_to_dict, get_filetype_with_magica
from src.parser.mapping_util import map_a_dict
from src.Preprocessor import Preprocessor


class InputReader:
    """
    The input reader for MRI data following tomo_mapper architecture.
    
    Implementation concept:
    - fail early: z.b errors in mapping file can be handled before starting to extract any file content.
    - reject with error
    - warn about unusual input
    """

    def __init__(self, map_path, input_path):
        logging.info("Preparing MRI parser based on mapping file and input.")
        
        # Read and parse the mapping file
        self.mapping_dict = MapFileReader.read_mapfile(map_path)
        
        # Parse different sections for different purposes
        self.study_mapping = MapFileReader.parse_mapinfo_for_study(self.mapping_dict)
        self.series_mapping = MapFileReader.parse_mapinfo_for_series(self.mapping_dict)
        self.perImage_mapping = MapFileReader.parse_mapinfo_for_perImage(self.mapping_dict)
        
        # Validate input file exists
        if not os.path.exists(input_path):
            logging.error("Input file {} does not exist. Aborting".format(input_path))
            raise MappingAbortionError("Input file loading failed.")
        
        self.input_path = input_path
        
        # Check if MRI parser can handle this file
        self.parser_names = self.get_applicable_parsers(input_path)
        if not self.parser_names:
            logging.error("No applicable parsers found for input {}".format(input_path))
            raise MappingAbortionError("Input file parsing aborted.")
        
        logging.info("Applicable parsers: {}".format(", ".join(self.parser_names)))

    @staticmethod
    def get_applicable_parsers(input_path):
        """
        Filters the available image parsers to those applicable to the input file format.
        :param input_path: file path to input
        :return: list of parser names that can handle the provided input format
        """
        
        filetype = get_filetype_with_magica(input_path)
        logging.debug("Determined input type: {}".format(filetype))

        available_parsers = []
        for k, p in ParserFactory.available_img_parsers.items():
            expected = p.expected_input_format()
            if filetype in expected:
                available_parsers.append(k)
        return available_parsers

    def retrieve_image_info(self):
        """
        Applies the applicable parser to extract MRI metadata.
        :return: dictionary containing the mapped metadata
        """
        for parser in self.parser_names:
            logging.debug("Trying to parse image with {}".format(parser))
            imgp = ParserFactory.create_img_parser(parser)

            # Combine all mappings for the parser
            combined_mapping = {}
            combined_mapping.update(self.study_mapping)
            combined_mapping.update(self.series_mapping)
            combined_mapping.update(self.perImage_mapping)

            result, raw = imgp.parse(self.input_path, combined_mapping)
            if result and result.image_metadata:
                output_dict = result.image_metadata.to_schema_dict()
                return output_dict

        logging.error("No parser could successfully process the input file")
        raise MappingAbortionError("Image parsing failed.")