import logging
import os.path
from json import JSONDecodeError
from urllib.parse import urlparse

from requests import HTTPError

from src.IO.MappingAbortionError import MappingAbortionError
from src.parser.ParserFactory import ParserFactory
from src.util import load_json

import validators


class MapFileReader:
    """
    This class provides utility functions reading and checking the user-provided map for MRI data
    """

    @staticmethod
    def read_mapfile(filepath) -> dict:
        """
        Load local or remote map file into dict
        :param filepath: local absolute path, local relative path or remote (absolute) URI
        :return: file content as dict
        """
        logging.info("Reading map file content")
        try:
            return load_json(filepath)
        except HTTPError as e:
            logging.error("Tried loading remote mapping file: {}".format(filepath))
            logging.error(e)
            raise MappingAbortionError("Map file loading failed.")
        except FileNotFoundError as e:
            logging.error("Local map file does not exist: {}".format(filepath))
            logging.error(e)
            raise MappingAbortionError("Map file loading failed.")
        except UnicodeDecodeError as e:
            logging.error("Unable to load map file as json. Please check file and file encoding")
            raise MappingAbortionError("Map file loading failed.")
        except JSONDecodeError as e:
            logging.error("Unable to load map file as json. Please check file structure")
            raise MappingAbortionError("Map file loading failed.")

    @staticmethod
    def parse_mapinfo_for_study(mapping_dict: dict):
        """
        Parse mapping dictionary to extract study-related mapping information
        :param mapping_dict: the full mapping dictionary
        :return: study mapping dictionary
        """
        if 'study' in mapping_dict:
            return mapping_dict['study']
        else:
            logging.warning("No study section found in mapping file")
            return {}

    @staticmethod
    def parse_mapinfo_for_series(mapping_dict: dict):
        """
        Parse mapping dictionary to extract series-related mapping information
        :param mapping_dict: the full mapping dictionary
        :return: series mapping dictionary
        """
        if 'series' in mapping_dict:
            return mapping_dict['series']
        else:
            logging.warning("No series section found in mapping file")
            return {}

    @staticmethod
    def parse_mapinfo_for_perImage(mapping_dict: dict):
        """
        Parse mapping dictionary to extract per-image-related mapping information
        :param mapping_dict: the full mapping dictionary
        :return: perImage mapping dictionary
        """
        if 'perImage' in mapping_dict:
            return mapping_dict['perImage']
        else:
            logging.warning("No perImage section found in mapping file")
            return {}