from .map_schema import Map_Schema


class Map_MRI_Schema(Map_Schema):

    def __init__(self, schema_skeleton: dict, key_list: list, map: object):
        """Takes the schema structure as dictionary and the metadata map to assign the metadata values to the schema attributes
        at the proper hirarchy level. Inherits from the Map_Schema class.

        Args:
            schema_skeleton (dict): The dictionary containing the skeleton of the target schema.
            key_list (list): The list that contains all keys of the schema skeleton at the first hierarchy level.
            map (object): The object that represents the mapped attributes.
        """

        super().__init__(schema_skeleton, key_list, map)

    # This method parses the objects in the schema structure and calls the proper method to insert the attribute value, based on the attribute type. Has additional functionality for value and unit attributes from the MRI schema
    def fill_json_object(self, json_object: dict, key_list: list, attributes_object: list):
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
            if (type(json_object[key]) == type(str()) or type(json_object[key]) == type(tuple())):

                if key in attributes_object.__dict__.keys():
                    new_dict[key] = self.get_json_type(json_object[key], attributes_object.__dict__[key])
                elif (key == "unit") and ("value" in new_dict):
                    new_dict[key] = json_object[key]
                else:
                    pass
            elif type(json_object[key]) == type(dict()):
                if (key in attributes_object.__dict__) and (isinstance(attributes_object.__dict__[key], type)):
                    sub_dict = self.fill_json_object(json_object[key], list(json_object[key].keys()), attributes_object.__dict__[key])
                else:
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