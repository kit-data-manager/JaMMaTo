import logging

from mappingservice_plugincore.IO.BaseInputReader import BaseInputReader
from mappingservice_plugincore.parser.ParserFactory import ParserFactory
from mappingservice_plugincore.file_util import is_zipfile, extract_zip_file

from src.IO.MapfileReader import MapFileReader

class InputReader(BaseInputReader):

    def __init__(self, map_path: str, input_path: str):
        super().__init__(map_path, input_path)
        logging.info("Preparing MRI parser based on mapping file and input.")

        # Read and parse the mapping file
        self.mapping_dict = MapFileReader.read_mapfile(map_path)
        self.mapping = self.mapping_dict

        # Parse different sections for different purposes
        self.temp_dir_path = None
        self.working_dir_path = input_path

        if is_zipfile(input_path):
            logging.info("ZIP input detected. Extracting MRI dataset.")

            self.temp_dir_path = extract_zip_file(input_path)
            self.working_dir_path = self.temp_dir_path

        logging.debug(
            f"MRI working directory/input: {self.working_dir_path}"
        )

    def retrieve_image_info(self):
        """
        Parse the MRI input.

        For a single DICOM file, working_dir_path points to the DICOM file.
        For a ZIP archive, working_dir_path points to the extracted directory.

        The MRI parser is responsible for reading all DICOM files belonging
        to the study and for grouping them by StudyInstanceUID and
        SeriesInstanceUID.
        """

        parser = ParserFactory.create_img_parser("MRI_Parser")

        result, raw = parser.parse(
            self.working_dir_path,
            self.mapping
        )

        if result is None:
            logging.warning("No MRI metadata could be extracted.")
            return None

        if result.image_metadata is None:
            logging.warning("MRI parser returned no image metadata.")
            return None

        return result.image_metadata.to_schema_dict()