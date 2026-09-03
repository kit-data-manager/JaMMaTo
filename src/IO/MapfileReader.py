import logging
from json import JSONDecodeError

from requests import HTTPError

from mappingservice_plugincore.exceptions.MappingAbortionError import MappingAbortionError
from mappingservice_plugincore.file_util import load_json


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