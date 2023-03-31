from typing import Any
import logging
from .attribute_mapper import Attribute_Mapper

class Attribute_Inserter():

    def __init__(self, schema_skeleton: dict, key_list: list, map: object) -> None:
        """Takes the schema structure as dictionary and the metadata map to assign the metadata values to the schema attributes
        at the proper hirarchy level of the JSON schema.

        Args:
            schema (dict): The dictionary containing the skeleton of the target schema.
            key_list (list): The list that contains all keys of the schema skeleton at the first hierarchy level.
            map (object): The object that represents the mapped attributes.
        """
        self.schema_skeleton = schema_skeleton
        self.key_list = key_list
        self.map = map

    def fill_json_object(self, json_object: dict, key_list: list, attributes_object: object):
        """Takes the JSON object of the schema structure, the key list of the current schema hierarchy level and the attributes object. 
        Calls the proper method to insert the attribute value, based on the attribute type. Has in addition a functionality for inserting
        the value of the main key string of an JSON object containing value and unit properties.

        Args:
            json_object (dict): The dictionary containing the skeleton of the target schema.
            key_list (list): The list that contains all keys of the schema skeleton at the first hierarchy level.
            attributes_object (object): The object that contains the mapped attributes.

        Returns:
            dict: The dictionary that represents the filled JSON object.
        """
        new_dict = {}

        for key in key_list:
            if (isinstance(json_object[key], str)) or (isinstance(json_object[key], tuple)):
                if key in attributes_object.keys():
                    new_dict[key] = self.get_json_type(json_object[key], attributes_object[key])
                else:
                    new_dict[key] = self.get_json_type(json_object[key], json_object[key])
            elif isinstance(json_object[key], dict):
                if key in attributes_object:
                    if isinstance(attributes_object[key], Attribute_Mapper):
                        sub_dict = self.fill_json_object(json_object[key], list(json_object[key].keys()), attributes_object[key].__dict__)
                    else:
                        sub_dict = self.fill_json_object(json_object[key], list(json_object[key].keys()), attributes_object[key])
                else:
                    sub_dict = self.fill_json_object(json_object[key], list(json_object[key].keys()), attributes_object)
                if len(sub_dict) > 0:
                    new_dict[key] = sub_dict
            elif isinstance(json_object[key], list):
                filled_array=[]
                if key in attributes_object:
                        filled_array = self.fill_json_array(json_object, key, json_object[key], attributes_object[key])
                else:
                    pass
                if len(filled_array) > 0:
                    new_dict[key] = filled_array
                else:
                    pass
            else:
                pass
        return new_dict

    def fill_json_array(self, json_object: dict, json_object_property: str, json_array: list, attributes: Any) -> list:
        """Takes the json object of the schema structure, the property that contains the json array as value, the json array and the attributes, either as object, or list of objects.
        Parses the array in the schema structure and calls the proper method to insert the attribute value, based on the attribute type.

        Args:
            json_object (dict): The dictionary that represents the schema skeleton object.
            json_object_property (str): The string property that contains the json array as value.
            json_array (list): The list that represents the schema skeleton array.
            attributes (Any): The object that contains the mapped attributes, or a list of objects that contain the mapped attributes.

        Returns:
            list: The list that represents the filled json array.
        """
        if isinstance(attributes, list) == False:
            if json_object_property in attributes.__dict__.keys():
                attributes = attributes.__dict__[json_object_property]
        try:
            json_array = json_array * len(attributes)
        except TypeError as e:
            logging.warning(e)
            pass

        new_list = []

        for list_item, list_index in zip(json_array, range(0, len(json_array))):
            if (isinstance(list_item, str)) or (isinstance(list_item, tuple)):
                try:
                    new_list.append(self.get_json_type(list_item, attributes[list_index]))
                except TypeError as e:
                    logging.warning(e)
                    pass
            elif isinstance(list_item, dict):
                if isinstance(attributes[list_index], Attribute_Mapper):
                    new_list.append(self.fill_json_object(list_item, list(
                    list_item.keys()), attributes[list_index].__dict__))
                else:
                    new_list.append(self.fill_json_object(list_item, list(
                        list_item.keys()), attributes[list_index]))
            elif isinstance(list_item, list):
                new_list.append(self.fill_json_array(json_object, json_object_property, list_item, attributes[list_index]))
            else:
                pass
        return new_list

    def get_json_type(self, data_type: str, attribute: str) -> Any:
        """Takes an attribute and its data type. Confirms the primitive data types of the mapped attribute values and assigns these values to the schema attribute. The correct hirarchial
        position has been reached through the methods above.

        Args:
            data_type (str): The string that representes the data type for an attribute.
            attribute (str): The string that represents the value of the mapped attribute.

        Returns:
            Any: The value of the mapped attribute as the correct data type.
        """
        try:
            if (isinstance(data_type, tuple) and (isinstance(attribute, tuple)==False)):
                if (isinstance(attribute, list)) and ("<class 'list'>" in data_type):
                    return attribute
                else:
                    for element in data_type:
                        if element in ["<class 'int'>", "<class 'bool'>", "<class 'None'>", "<class 'float'>", "<class 'list'>"]:
                            return (self.get_json_type(element, attribute))
                        else:
                            pass
                    logging.warning(f'incorrect type provided for {attribute}, expected {data_type} but received {type(attribute)}, returning original value.')
                    return attribute
            elif isinstance(attribute, tuple):
                logging.warning(f'No value provided for {attribute}, returning original value.')
                return attribute
            elif data_type == "<class 'int'>":
                return int(attribute)
            elif data_type == "<class 'bool'>":
                return bool(attribute)
            elif data_type == "<class 'None'>":
                return "null"
            elif data_type == "<class 'float'>":
                return float(attribute)
            elif data_type == "<class 'str'>":
                return str(attribute)
            else:
                logging.warning(f'incorrect type provided for {attribute}, expected {data_type} but received {type(attribute)}, returning original value.')
                return attribute
        except TypeError as e:
            logging.warning(f'incorrect type provided for {attribute}, expected {data_type} but received {type(attribute)}, returning original value.')
            return attribute
        except ValueError as e:
            logging.warning(f'incorrect value provided for {attribute}, expected {data_type} but received {type(attribute)}, returning original value.')
            return attribute