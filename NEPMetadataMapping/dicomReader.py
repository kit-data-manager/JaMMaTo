import pydicom
import re
import logging
from datetime import datetime
# This class instantiates the class object of a dicom file, which contains the key-value pairs of the fiel metadata.


class DicomReader:

    def __init__(self, dicom_file: str) -> None:
        """Takes a dicom file as input and converts the file into a Python object using the pydicom module.

        Args:
            dicom_file (str): String that contains the location to the dicom file.
        """
        try:
            self.pydicom_file = pydicom.dcmread(dicom_file)
        except TypeError as e:
            logging.warning("Error for file: %s %s", dicom_file, e)
            self.pydicom_file = pydicom.dcmread(dicom_file, force=True)
        except FileNotFoundError as e:
            logging.warning("No valid Dicom file: %s %s", dicom_file, e)
            self.pydicom_file=None
        if self.pydicom_file:
            self.studyDateTime = None
            self.sub_dict=self.pydicom_object_search(self.pydicom_file)
            self.sub_dict.pop("pixelData")
            self.__dict__.update(self.sub_dict)
            self.studyDateTime = datetime.strptime(
                self.studyDateTime, '%Y%m%d %H%M%S').isoformat()
            self.__dict__.pop("sub_dict")
            self.__dict__.pop("pydicom_file")
        else:
            pass
    def pydicom_object_search(self, dataset: pydicom) -> dict:
        """Takes as input a pydicom object and searches its attributes. Puts the attributes which contain a string as value, or a list of values into a dictionary.

        Args:
            dataset (pydicom): The pydicom object that contains all attributes of a dicom file in a nested structure.

        Returns:
            dict: The dictionary that contains the dicom attributes in a flat structure as key-value pairs.
        """
        sub_dict = {}
        for attribute in dataset:
            if self.validate_type(attribute, pydicom.Dataset):
                sub_dict=self.pydicom_object_search(attribute)
            elif self.validate_type(attribute.value, pydicom.Sequence):
                name=self.name_standardization(attribute.name)
                if len(attribute.value) > 1:
                    mergedsub_dict={}
                    for value in attribute.value:
                        subsub_dict=(self.pydicom_object_search(value))
                        mergedsub_dict=self.merge_dict_keys(subsub_dict, mergedsub_dict)
                    sub_dict.update(mergedsub_dict)
                    
                else:
                    sub_dict.update(self.pydicom_object_search(attribute.value))
            else:
                name=self.name_standardization(attribute.name)
                if name == "studyDate":
                    self.studyDateTime = attribute.value + " "
                if name == "studyTime":
                    self.studyDateTime += attribute.value
                
                sub_dict[name] = attribute.value
        return sub_dict

    def name_standardization(self, attribute: str) -> str: 
        """Takes a string of a dicom attribute as input and standardizes it after defined criteria.

        Args:
            attribute (str): The attribute string that should be standardized.

        Returns:
            str: The attribute string after standardization.
        """
        name = attribute.split()
        if len(name) == 1:
            name = name[0].lower()
        else:
            subname = ""
            for letter in name[1:]:
                subname += letter.capitalize()
            name = name[0].lower() + subname
        name = re.sub('[^A-Za-z0-9]+', '', name)
        return name

    def merge_dict_keys(self, subsub_dict: dict, mergedsub_dict: dict) -> dict:
        """Takes as input a two dictionaries that contain attributes of a repeating attribute sequence in the pydicom file. It merges the file contains and returns one dictionary that
        has a list of values from both dictionaries for each key in the new dictionary.

        Args:
            subsub_dict (dict): The dictionary with the new values for each key.
            mergedsub_dict (str): The dictioanry with the current values in a list for each key.

        Returns:
            dict: The merged dictionary of both input dictionaries.
        """
        new_mergedsub_dict={}
        dict_keys = [key for key in subsub_dict.keys()]
        try:
            for key in dict_keys:
                if isinstance(mergedsub_dict[key], list):
                    mergedsub_dict[key].append(subsub_dict[key])
                    new_mergedsub_dict[key] = mergedsub_dict[key]
                else:
                    new_mergedsub_dict[key] = [mergedsub_dict[key], subsub_dict[key]]
        except KeyError as e:
            new_mergedsub_dict = subsub_dict
        return new_mergedsub_dict

    def validate_type(self, attribute: str, instance: object):
        return isinstance(attribute, instance)

#test=DicomReader("/Users/nicoblum/bwSyncShare/NEP/DicomTestStudy/Series/series7.dcm")
#print(test.__dict__)