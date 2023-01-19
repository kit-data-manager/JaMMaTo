import os
import logging
import zipfile
import pydicom
from .dicom_reader import Dicom_Reader

class Metadata_Reader():

    def __init__(self, metadata_document_directory: str) -> None:
        """Takes the path to either a single document that contains the metadata for mapping, or 
        to a folder that contains multiple corresponding files with metadata.

        Args:
            metadata_document_directory (str): String path to the metadata files.
        """
        self.all_dicom_series = []
        #is_file = os.path.isfile(metadata_document_directory)
        #is_directory = os.path.isdir(metadata_document_directory)
        file_name, file_extension = os.path.splitext(
                metadata_document_directory)

        if file_extension == ".zip":
            file_name, file_extension = os.path.splitext(
                metadata_document_directory)
            with zipfile.ZipFile(metadata_document_directory) as dataset:
                for file in range(1, len(dataset.filelist)):
                    with dataset.open(dataset.filelist[file].filename) as file:
                        datasetFileName, dataset_file_extension = os.path.splitext(
                            file.name)
                        self.evaluate_file_type(
                            file, dataset_file_extension)

        elif type(file_extension) == type(str()):
            self.evaluate_file_type(metadata_document_directory, file_extension)
        else:
            logging.error("No valid metadata file path.")
            raise FileNotFoundError("No valid metadata file path.")
            
    def evaluate_file_type(self, file: str, file_extension: str) -> None:
        """Takes the file path and the file extension and evaluates their type in order to call the corresponding class for metadata 
        extraction.

        Args:
            file (str): String path to the metadata file.
            file_extension (str): String of the file type.
        """
        if file_extension == ".dcm":
            try:
                dicom_series = Dicom_Reader(file)
                self.all_dicom_series.append(dicom_series)
            except pydicom.errors.InvalidDicomError as e:
                pass
            except FileNotFoundError as e:
                pass
        else:
            logging.error("File format is not supported.")
