# This class takes the schema structure as json_object and the metadata map to assign the metadata values to the schema attributes
# at the proper hirarchy level.
from typing import Any
import logging

class MapSchema:

    def __init__(self, schema_skeleton: dict, key_list: list, map: object) -> None:
        """Instantiates the components for placing the mapped attributes at the correct position in the json schema.

        Args:
            schema (dict): The dictionary that represents the schema skeleton.
            key_list (list): The list that contains all keys of the schema skeleton at the first hierarchy level.
            map (object): The object that represents the mapped attributes.
        """

        self.schema_skeleton = schema_skeleton
        self.key_list = key_list
        self.map = map

    def fill_json_object(self, json_object: dict, key_list: list, attributes_object: object) -> dict:
        """Takes the json object of the schema structure, the key list of the current schema hierarchy level and the attributes object. 
        Calls the proper method to insert the attribute value, based on the attribute type.

        Args:
            json_object (dict): The dictionary that represents the schema skeleton object.
            key_list (list): The list that contains all keys of the schema skeleton at the first hierarchy level.
            attributes_object (object): The object that contains the mapped attributes.

        Returns:
            dict: The dictionary that represents the filled json object.
        """
        new_dict = {}

        for key in key_list:
            if (type(json_object[key]) == type(str()) or type(json_object[key]) == type(tuple())):

                if key in attributes_object.__dict__.keys():
                    new_dict[key] = self.get_json_type(json_object[key], attributes_object.__dict__[key])
                else:
                    pass
            elif type(json_object[key]) == type(dict()):
                sub_dict = self.fill_json_object(json_object[key], list(json_object[key].keys()), attributes_object)
                if len(sub_dict) > 0:
                    new_dict[key] = sub_dict
            elif type(json_object[key]) == type(list()):
                filled_array = self.fill_json_array(json_object, key, json_object[key], attributes_object)
                if len(filled_array) > 0:
                    new_dict[key] = filled_array
                else:
                    pass
            else:
                pass
        return new_dict

    # This method 
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
        if type(attributes) != type(list()):
            if json_object_property in attributes.__dict__.keys():
                attributes = attributes.__dict__[json_object_property]
        try:
            json_array = json_array * len(attributes)
        except TypeError as e:
            logging.warning(e)
            pass

        new_list = []

        for list_item, list_index in zip(json_array, range(0, len(json_array))):
            if type(list_item) == type(str()):
                try:
                    new_list.append(self.get_json_type(list_item, attributes[list_index]))
                except TypeError as e:
                    logging.warning(e)
                    pass
            elif type(list_item) == type(dict()):
                new_list.append(self.fill_json_object(list_item, list(
                    list_item.keys()), attributes[list_index]))
            elif type(list_item) == type(list()):
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
        if isinstance(data_type, tuple):
            return (self.get_json_type(data_type[0], attribute))
        elif data_type == "int":
            return int(attribute)
        elif data_type == "bool":
            return bool(attribute)
        elif data_type=="None":
            return "null"
        elif data_type == "float":
            return float(attribute)
        else:
            return str(attribute)
