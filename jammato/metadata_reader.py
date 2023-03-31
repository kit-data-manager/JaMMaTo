import os
import logging
import zipfile
import pydicom
from typing import Any

from .dicom_reader import Dicom_Reader
from .analyse_study import Analyse_Study
from .data_cleaning import data_cleaning_instance

class Metadata_Reader():

    def __init__(self, metadata_document_directory: str, config_dicom_file_validation) -> None:
        """Takes the path to either a single document that contains the metadata for mapping, or 
        to a folder that contains multiple corresponding files with metadata.

        Args:
            metadata_document_directory (str): String path to the metadata files.
        """
        self.analyse_study_instance=Analyse_Study(config_dicom_file_validation)
        self.all_dicom_series_dict={}
        self.all_dicom_series = []
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
                
                for value in self.all_dicom_series_dict.values():
                    if len(value)>1:
                        self.all_dicom_series.extend(self.post_read_processing(value, flag="all"))
                    else:
                        self.all_dicom_series.extend(self.post_read_processing(value, flag="single"))

        elif type(file_extension) == type(str()):
            self.evaluate_file_type(None, metadata_document_directory, file_extension)
        else:
            logging.error("No valid metadata file path.")
            raise FileNotFoundError("No valid metadata file path.")
        return

    def evaluate_file_type(self, file: str, file_extension: str) -> None:
        """Takes the file path and the file extension and evaluates their type in order to call the corresponding class for metadata 
        extraction.

        Args:
            file_num (str): String path to the metadata file.
            file_extension (str): String of the file type.
        """

        if file_extension == ".dcm":
            try:
                dicom_series = Dicom_Reader(file)
                sub_dict=Dicom_Reader.pydicom_object_search(dicom_series.pydicom_file)
                dicom_series.__dict__.update(sub_dict)
                del dicom_series.pydicom_file

                duplicate_sop_elements, duplicate_series_elements=self.analyse_study_instance.analyse_study(dicom_series)
                if (duplicate_sop_elements==False) and (duplicate_series_elements==True):
                    self.all_dicom_series_dict[dicom_series.__dict__[self.analyse_study_instance.file_series_instance_uid]].append(dicom_series)
                else:
                    self.all_dicom_series_dict[dicom_series.__dict__[self.analyse_study_instance.file_series_instance_uid]]=[dicom_series]

            except pydicom.errors.InvalidDicomError as e:
                pass
            except FileNotFoundError as e:
                pass
        else:
            logging.error("File format is not supported.")
        return

    def post_read_processing(self, attributes: Any, flag):
        data_cleaning_instance.load_attributes(attributes)
        if flag=="single":
            data_cleaning_instance.set_attributes_from_config(flag="single")
        elif flag=="all":
            data_cleaning_instance.set_attributes_from_config(flag="all")
        else:
            raise("No correct flag provided.")
        return data_cleaning_instance.attributes_dict
            