import logging
from typing import Any

class Schema_Reader():

    def __init__(self, schema: dict) -> None:
        """Instantiates the class that searches the schema structure of the provided dictionary and builds a schema skeleton. When instantiated, the json definitions are first set.

        Args:
            schema (dict): The json schema document as dictionary.
        """
        if "$defs" in schema.keys():
            self.definitions = schema["$defs"]
        elif "definitions" in schema.keys():
            self.definitions = schema["definitions"]
        else:
            self.definitions = None
        self.schema = schema

    def json_definition_search(self, definition: dict) -> dict:
        """Takes a dictionary as input that represents the reference to a json definition as content. Returns the skeleton of this content as a dictionary.

        Args:
            definition (dict): The reference content as dictionary.

        Returns:
            dict: The skeleton of the reference content as dictionary.
        """
        properties = None
        if "$ref" in definition:
            if definition["$ref"].startswith("#"):
                keyword = definition["$ref"].split("/")[-1:][0]
                sub_properties = self.json_definition_search(self.definitions[keyword])
                properties = sub_properties
            else:
                path = definition["$ref"]
                logging.warning("No correct definition path for " + path)
        elif "oneOf" in definition:
            sub_properties=self.one_of_search(definition)
            properties = sub_properties
        elif definition["type"] == "array":
            sub_properties = self.json_array_search(definition["items"])
            properties = sub_properties
        elif definition["type"] == "object":
            sub_properties = self.json_object_search(definition)
            properties = sub_properties
        else:
            properties = self.json_type_search(definition["type"])
        return properties

    def json_array_search(self, property: dict) -> list:
        """Takes a dictionary as input that represents the array type content of a json document. Returns the skeleton of this content as a list.

        Args:
            property (dict): The array type content as dictionary.

        Returns:
            list: The skeleton of the array type content as list.
        """
        properties = None
        if "$ref" in property:
            if property["$ref"].startswith("#"):
                keyword = property["$ref"].split("/")[-1:][0]
                sub_properties = [self.json_definition_search(self.definitions[keyword])]
                properties = sub_properties
            else:
                path = property["$ref"]
                logging.warning("No correct definition path for " + path)
        elif "oneOf" in property:
            sub_properties=self.one_of_search(property)
            properties = sub_properties
        elif property["type"] == "array":
            sub_properties = [self.json_array_search(property["items"])]
            properties = sub_properties
        elif property["type"] == "object":
            sub_properties = [self.json_object_search(property)]
            properties = sub_properties
        else:
            sub_properties = [self.json_type_search(property["type"])]
            properties = sub_properties
        return properties

    def json_object_search(self, property: dict) -> dict:
        """Takes a dictionary as input that represents the object type content of a json document. Returns the skeleton of this content as a dictionary.

        Args:
            property (dict): The object type content as dictionary.

        Returns:
            dict: The skeleton of the object type content as list.
        """
        properties = {}
        for i in property["properties"].items():
            if "$ref" in i[1]:
                if i[1]["$ref"].startswith("#"):
                    keyword = i[1]["$ref"].split("/")[-1:][0]
                    sub_properties = self.json_definition_search(self.definitions[keyword])
                    properties[i[0]] = sub_properties
                else:
                    path = i[1]["$ref"]
                    logging.warning("No correct definition path for " + path)
            elif "oneOf" in i[1]:
                sub_properties=self.one_of_search(i[1])
                properties[i[0]] = sub_properties
            elif i[1]["type"] == "array":
                sub_properties = self.json_array_search(i[1]["items"])
                properties[i[0]] = sub_properties
            elif i[1]["type"] == "object":
                sub_properties = self.json_object_search(i[1])
                properties[i[0]] = sub_properties
            else:
                if i[0] == "value":
                    properties[i[0]] = self.json_type_search(i[1]["type"])
                elif i[0] == "unit":
                    try:
                        properties[i[0]] = i[1]["default"]
                    except KeyError:
                        logging.warning("No default unit")
                        properties[i[0]] = self.json_type_search(i[1]["type"])
                else:
                    properties[i[0]] = self.json_type_search(i[1]["type"])
        return properties

    def json_type_search(self, type: str) -> Any:
        """Takes a string as input that represents the type of a json document, i.e. a primitive data type or a string. 
        The input string is altered and returned either as a string, or a list, if multiple types are present 

        Args:
            type (str): The string of the json type.

        Returns:
            Any: The string of the Python type, or a list of Python types as strings.
        """
        if type == "integer":
            return "<class 'int'>"
        elif type == "string":
            return "<class 'str'>"
        elif type == "number":
            return "<class 'float'>"
        elif type == "boolean":
            return "<class 'bool'>"
        elif type == "null":
            return "<class 'NoneType'>"
        elif type == "array":
            return "<class 'list'>"
        elif isinstance(type, list):
            multiple_types = []
            for j in type:
                multiple_types.append(self.json_type_search(j))
            return tuple(multiple_types)
        else:
            logging.warning("Type Error")
            return None
    
    def one_of_search(self, property: dict) -> list:
        """Takes a dictionary as input that represents the oneOf type content of a json document, which is an array of multiple possible values. 
        Returns the skeleton of this content as a list.

        Args:
            property (dict): The oneOf type content as dictionary.

        Returns:
            list: The skeleton of the oneOf type content as list.
        """
        sub_properties=[]
        for i in property["oneOf"]:
            if "items" in i:
                sub_sub_properties = self.json_array_search(i["items"])
                sub_properties.append(sub_sub_properties)
                properties=sub_properties
            elif "properties" in i:
                sub_sub_properties = self.json_object_search(i)
                sub_properties.append(sub_sub_properties)
                properties=sub_properties
            elif "type" in i: 
                sub_sub_properties = self.json_type_search(i["type"])
                sub_properties.append(sub_sub_properties)
                properties=sub_properties
            else:
                sub_properties=[None]
                properties=sub_properties
                logging.warning("No correct definition for \"oneOf\" attribute")
        return properties

