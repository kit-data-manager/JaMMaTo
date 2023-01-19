class Attribute_Mapping():

    def __init__(self, attributes: dict) -> None:
        """Instantiates the class and updates the attributes.

        Args:
            attributes (dict): Dictionary that contains the attributes to be updated.
        """
        self.__dict__.update(attributes)

    def Some():
        return ""

    @classmethod
    def mapping_from_object(cls, metadata_attributes: dict, map_dict: dict, map_main_attribute: str) -> dict:
        """Takes the metadata object as dictionary and the corresponding map dictionary to insert the proper values for a main attribute from the
        map dictionary.

        Args:
            metadata_attributes (dict): Dictionary of attributes from the metadata object.   
            map_dict (dict): Dictionary of the map for the origin and target schemas.
            map_main_attribute (str): The main attribute of the map dictionary (usually study, series and perImage) for which all attributes should be mapped.

        Returns:
            dict: The dictionary with the mapped attributes. Passes to the __init__ function, which updates the attributes.
        """
        temp={}
        for key, value in map_dict[map_main_attribute].items():
            if key in metadata_attributes:
                if "." in value:
                    split_values=value.split(".")
                    split_values.append(metadata_attributes[key])
                    for index in range(len(split_values)-1, 1, -1):
                        value_dict={}
                        value_dict[split_values[index-1]]= split_values[index]
                        split_values.remove(split_values[index])
                        split_values.remove(split_values[index-1])
                        value_dict=type('value_dict_object', (object,), value_dict)
                        split_values.append(value_dict)

                    temp[split_values[0]]=value_dict
                else:
                    temp[value]= metadata_attributes[key]
            else:
                pass
        return cls(temp)

    def update_map(self, **kwargs) -> None:
        """Takes a variable length of arguments that are used as dictionary to update the class object attributes.
        """
        self.__dict__.update(kwargs)
