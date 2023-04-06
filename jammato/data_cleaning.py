import json
from datetime import datetime
import os
from typing import Any
from collections.abc import Iterable

class Data_Cleaning():

    def __init__(self) -> None:
        """Instantiates the Data_Cleaning class and creates an empty attribute attribute_dict to be updatet.
        """
        self.config={}

    @classmethod
    def merge_date_time(cls, args: list, object_iterable: Any) -> dict:
        """Merge date and time values from two attributes into one attribute value.

        Args:
            args (list): Names of the original and merged attributes.
            attribute_dict (dict): The dictionry containing the key-value pairs of the attributes to be merged.

        Returns:
            dict: The updatet dictionary containing the merged attribute key-value pair.
        """
        for object in object_iterable:
            input_args=args[0]
            output_args=args[1]
            merged_date_time = object.__dict__[input_args[0]] + " "
            merged_date_time += object.__dict__[input_args[1]]
            try:
                merged_date_time = datetime.strptime(
                    merged_date_time, '%Y%m%d %H%M%S').isoformat()
            except:
                merged_date_time=merged_date_time
            object.__dict__.pop(input_args[0])
            object.__dict__.pop(input_args[1])
            object.__dict__[output_args]=merged_date_time
        return object_iterable

    @classmethod
    def merge_min_max_values(cls, args: list, object_iterable: Any) -> dict:
        input_args=args[0]
        min_value=min([object.__dict__[input_args[0]] for object in object_iterable])
        max_value=max([object.__dict__[input_args[1]] for object in object_iterable])
        for object in object_iterable:
            object.__dict__[input_args[0]]=min_value
            object.__dict__[input_args[1]]=max_value
        return object_iterable
    
    @classmethod
    def transfer_to_list(cls, iterable_atribute: Iterable) -> list:
        """Transfers an iterable attribute to a list.

        Args:
            iterable_atribute (Iterable): The iterable attribute to be converted.

        Returns:
            list: The resulting list.
        """
        new_list=[]
        for value in iterable_atribute:
            if isinstance(value, list):
                new_list.append(cls.iterate_list(value))
            else:
                new_list.append(value)
        return new_list

    def set_attributes_from_config(self, flag, config_file_path: str=os.getcwd()+"/configs/config_data_cleaning.json",) -> None:
        """Uses the JSON config file for the data cleaning to assess the methods and respective attributes that need to be cleaned. Attributes 
        and methods are then iteratively called and executed. The object instance attribute attribute_dict is then updatet after each process.

        Args:
            config_file_path (str, optional): The relative path to the config file directory. Defaults to os.getcwd()+"/configs/config_data_cleaning.json".
        """
        with open(config_file_path, 'r') as f:
            config_file = json.load(f)
        for func_string, args in config_file.items():
            self.store_config(func_string, args)
            func = getattr(Data_Cleaning, func_string)
            temp_attribute_dict=func(args, self.attributes_dict)
            self.attributes_dict=temp_attribute_dict
        return

    def load_attributes(self, attributes_dict: dict) -> None:
        """Load a dictionary to update the attribute_dict object instance attribute.

        Args:
            attributes_dict (dict): The dictionary containing the key-value pairs for the data cleaning setps.
        """
        self.attributes_dict=attributes_dict
        return
    
    def store_config(self, func_string, args):
        self.config.update({func_string: args})
        return
    
data_cleaning_instance=Data_Cleaning()
