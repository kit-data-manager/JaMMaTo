import json
from typing import Any
from .dicom_reader import Dicom_Reader

class Analyse_Study():
    def __init__(self, config_dicom_file_validation):
        self.configuration_dicom_file_validation(config_dicom_file_validation)
        self.all_sop_instance_uids=[]
        self.study_instance_uid = None
        self.all_series_instance_uids= []
        self.series_id_dict={}

    def configuration_dicom_file_validation(self, config_dicom_file_validation: str) -> None:
        """Configuration of the attributes used in the dicom file validation.

        Args:
            config_dicom_file_validation (str): The direction to the config file.
        """
        with open(config_dicom_file_validation, 'r') as f:
            dicom_file_validation_attributes = json.load(f)
        self.file_study_instance_uid=list(dicom_file_validation_attributes.values())[0]
        self.file_sop_instance_uid=list(dicom_file_validation_attributes.values())[1]
        self.file_series_instance_uid=list(dicom_file_validation_attributes.values())[2]
        return

    def set_series(self, series_id: str, series_attributes: Any) -> None:
        """Add the attributes for each series in a dictionary containing the series id as key and the object/dictionary with attributes as value.

        Args:
            series_id (str): The string of the series id.
            series_attributes (Any): The object or dictionary containing the attributes of a series.
        """
        self.series_id_dict[series_id]=series_attributes
        return

    def get_series(self, series_id: str) -> Any:
        """Retrieves the object/dictionary containing the attributes of a series using the series id.

        Args:
            series_id (str): The string of the series id.

        Returns:
            Any: The object/dictionary containing the attributes.
        """
        return self.series_id_dict[series_id]

    def analyse_study(self, series: Dicom_Reader) -> bool:
        """Validate that all dicom files (series) of a study have the same Study Instance UID.

        Args:
            dicom_object (MetadataReader): The object that contains the dicom metadata attributes.

        Raises:
            Exception: Strings are not the same.
        
        Returns:
            bool: Returns the boolean of the assessment if the ids are duplicates.
        """
        if (self.study_instance_uid != None) and (self.study_instance_uid != series.__dict__[self.file_study_instance_uid]):
            raise Exception('Files are not from the same study')
        else:
            self.study_instance_uid = series.__dict__[self.file_study_instance_uid]

        duplicate_sop_elements= series.__dict__[self.file_sop_instance_uid] in self.all_sop_instance_uids
        duplicate_series_elements= series.__dict__[self.file_series_instance_uid] in self.all_series_instance_uids
        self.all_sop_instance_uids.append(series.__dict__[self.file_sop_instance_uid])
        self.all_series_instance_uids.append(series.__dict__[self.file_series_instance_uid])
        return duplicate_sop_elements, duplicate_series_elements