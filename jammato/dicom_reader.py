import pydicom
import re
import logging
from .data_cleaning import data_cleaning_instance

class Dicom_Reader():

    def __init__(self, dicom_file: str) -> None:
        """Takes a dicom file as input and converts the file into a Python object using the pydicom module.

        Args:
            dicom_file (str): String that contains the location to the dicom file.
        """
        try:
            self.pydicom_file = pydicom.dcmread(dicom_file)
        except pydicom.errors.InvalidDicomError as e:
            logging.error("InvalidDicomError for file: %s %s", dicom_file, e)
            raise
        except FileNotFoundError as e:
            logging.error("FileNotFoundError for file: %s %s", dicom_file, e)
            raise
        
    @classmethod
    def pydicom_object_search(cls, dataset: pydicom) -> dict:
        """Takes as input a pydicom object and searches its attributes. Puts the attributes which contain a string as value, or a list of values into a dictionary.

        Args:
            dataset (pydicom): The pydicom object that contains all attributes of a dicom file in a nested structure.

        Returns:
            dict: The dictionary that contains the dicom attributes in a flat structure as key-value pairs.
        """
        sub_dict = {}
        for attribute in dataset:
            if isinstance(attribute, pydicom.Dataset):
                sub_dict=cls.pydicom_object_search(attribute)
            elif isinstance(attribute.value, pydicom.Sequence):
                name=cls.name_standardization(attribute.name)
                if len(attribute.value) > 1:
                    mergedsub_dict={}
                    for value in attribute.value:
                        subsub_dict=(cls.pydicom_object_search(value))
                        mergedsub_dict=cls.merge_dict_keys(subsub_dict, mergedsub_dict)
                    sub_dict.update(mergedsub_dict)
                    
                else:
                    sub_dict.update(cls.pydicom_object_search(attribute.value))
            else:
                name=cls.name_standardization(attribute.name)
                if isinstance(attribute.value, pydicom.multival.MultiValue):
                    sub_dict[name]=data_cleaning_instance.transfer_to_list(attribute.value)
                elif isinstance(attribute.value, pydicom.valuerep.PersonName):
                        sub_dict[name]=str(attribute.value)
                elif isinstance(attribute.value, pydicom.uid.UID):
                        sub_dict[name]=str(attribute.value)
                elif isinstance(attribute.value, pydicom.valuerep.DSfloat):
                        sub_dict[name]=str(attribute.value)
                elif isinstance(attribute.value, pydicom.valuerep.IS):
                        sub_dict[name]=str(attribute.value)
                else:
                    sub_dict[name] = attribute.value
        return sub_dict

    @classmethod
    def name_standardization(cls, attribute: str) -> str: 
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

    @classmethod
    def merge_dict_keys(cls, subsub_dict: dict, mergedsub_dict: dict) -> dict:
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
                    if (isinstance(subsub_dict[key], list)) and (isinstance(mergedsub_dict[key][0], list)==False):
                        mergedsub_dict[key]=[mergedsub_dict[key]]
                    else:
                        pass
                    mergedsub_dict[key].append(subsub_dict[key])
                    new_mergedsub_dict[key] = mergedsub_dict[key]
                else:
                    new_mergedsub_dict[key] = [mergedsub_dict[key], subsub_dict[key]]
        except KeyError as e:
            new_mergedsub_dict = subsub_dict
        return new_mergedsub_dict