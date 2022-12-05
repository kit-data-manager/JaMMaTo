# This class takes the schema structure as dictionary and the metadata map to assign the metadata values to the schema attributes
# at the proper hirarchy level.
from .mapSchema import MapSchema


class Map_MRI_Schema(MapSchema):

    def __init__(self, schema_skeleton: dict, key_list: list, map: object, main_key: str):

        super().__init__(schema_skeleton, key_list, map)
        self.main_key=main_key

    # This method parses the objects in the schema structure and calls the proper method to insert the attribute value, based on the attribute type. Has additional functionality for value and unit attributes from the MRI schema
    def fill_json_object(self, json_object: dict, key_list: list, attributes_object: list, main_key: str=None):  # List or Dict?
        new_dict = {}

        # evaluate the types of the values of the keys (i.e. properties of JSON schema)
        for key in key_list:

            # key has a string as value
            if (type(json_object[key]) == type(str()) or type(json_object[key]) == type(tuple())):

                if key in attributes_object.__dict__.keys():
                    new_dict[key] = self.get_json_type(json_object[key], attributes_object.__dict__[key])
                elif (key == "value") and (main_key in attributes_object.__dict__):
                    new_dict[key] = self.get_json_type(json_object[key], attributes_object.__dict__[main_key])
                elif (key == "unit") and ("value" in new_dict):
                    new_dict[key] = json_object[key]
                else:
                    pass

            # key has an object as value
            elif type(json_object[key]) == type(dict()):
                sub_dict = self.fill_json_object(json_object[key], list(json_object[key].keys()), attributes_object, key)
                if len(sub_dict) > 0:
                    new_dict[key] = sub_dict

            # key has an array as value
            elif type(json_object[key]) == type(list()):
                # Special condition, very specific for the MRI schema
                if key == "value":
                    dictionary_copy = {}
                    dictionary_copy[main_key] = json_object.copy().pop(key)
                    rev_dict = dict(reversed(list(dictionary_copy.items())))
                    filled_array = self.fill_json_array(rev_dict, main_key, dictionary_copy[main_key], attributes_object)
                else:
                    filled_array = self.fill_json_array(json_object, key, json_object[key], attributes_object)
                if len(filled_array) > 0:
                    new_dict[key] = filled_array
                else:
                    pass
            else:
                pass
        return new_dict
