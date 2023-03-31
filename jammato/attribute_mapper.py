from typing import Any
import logging
from nested_lookup import nested_lookup

class Attribute_Mapper():

    def __init__(self, **kwargs) -> None:
        """Instantiates the class and updates the attributes.
        """
        if kwargs:
            self.__dict__.update(kwargs)
        else:
            pass
    
    def update_object_attributes(self, attributes: dict) -> None:
        """Updates the key-value pairs of the object attributes dictionary.

        Args:
            attributes (dict): Attributes to be added to the object dictionary.
        """
        self.__dict__.update(attributes)
        
        return 
    
    @classmethod
    def mapping_from_object(cls, metadata_attributes: dict, map_dict: dict, map_main_attribute: str, object_names: list) -> dict:
        """Takes the metadata object as dictionary and the corresponding map dictionary to insert the proper values for a main attribute from the
        map dictionary.

        Args:
            metadata_attributes (dict): Dictionary of attributes from the metadata object.   
            map_dict (dict): Dictionary of the map for the origin and target schemas.
            map_main_attribute (str): The main attribute of the map dictionary (usually study, series and perImage) for which all attributes should be mapped.

        Returns:
            dict: The dictionary with the mapped attributes. Passes to the __init__ function, which updates the attributes.
        """
        mapped_attribues={}
        for key, value in map_dict[map_main_attribute].items():
            if value in metadata_attributes:
                if "." in key:
                    split_keys=key.split(".")
                    split_keys.append(metadata_attributes[value])
                    split_keys=cls.remove_from_list(split_keys, object_names)
                    for index in range(len(split_keys)-1, 1, -1):
                        temp_key_dict={}
                        temp_key_dict[split_keys[index-1]]= split_keys[index]
                        split_keys.remove(split_keys[index])
                        split_keys.remove(split_keys[index-1])
                        split_keys.append(temp_key_dict)
                    if split_keys[0] in mapped_attribues:
                        merged_attribute_object=cls.merge_mapped_attributes(mapped_attribues[split_keys[0]], temp_key_dict)
                        mapped_attribues[split_keys[0]]=merged_attribute_object
                    else:
                        attribute_object=Attribute_Mapper()
                        attribute_object.update_object_attributes(temp_key_dict)
                        mapped_attribues[split_keys[0]]=attribute_object
                else:
                    mapped_attribues[key]= metadata_attributes[value]
            else:
                pass
        return mapped_attribues

    @classmethod
    def merge_mapped_attributes(cls, existing_attributes: Any, new_attributes: Any, list_attribute=None) -> object:
        """Merges the mapped attributes that belong to the same hirarchy in the target schema, by adding them to the same object.

        Args:
            existing_attributes (Any): The object, or dictionary containing the mapped attributes of the same schema hierarchy.
            new_attributes (Any): The object, or dictionary containing new attributes that need to be merged with the (object) dictionary of mapped attributes.
            list_attribute (_type_, optional): In case a list attribute exists that needs to be added to the attribute dictionary. Defaults to None.

        Returns:
            object: The object containing the merged new and existing mapped attributes.
        """
        temp_dict={}
        if isinstance(existing_attributes, Attribute_Mapper):
            attribute_dict=existing_attributes.__dict__
        else:
            attribute_dict=existing_attributes
        if isinstance(new_attributes, Attribute_Mapper):
            new_attributes=new_attributes.__dict__
        else:
            pass
        if list(new_attributes.keys())[0] == list_attribute:
            if list_attribute in attribute_dict:
                attribute_dict[list_attribute].append(new_attributes[list_attribute])
            else:
                attribute_dict[list_attribute]=[new_attributes[list_attribute]]
            attribute_object_1=Attribute_Mapper()
            attribute_object_1.update_object_attributes(attribute_dict)
            return attribute_object_1
        elif list(new_attributes.keys())[0] in (attribute_dict.keys()):
            attribute_dict[list(new_attributes.keys())[0]]=cls.merge_mapped_attributes(attribute_dict[list(new_attributes.keys())[0]], new_attributes[list(new_attributes.keys())[0]], list_attribute)
            if not isinstance(attribute_dict, Attribute_Mapper):
                attribute_object_1=Attribute_Mapper()
                attribute_object_1.update_object_attributes(attribute_dict)
            else:
                temp_dict[list(new_attributes.keys())[0]]=attribute_dict
                attribute_object_1=Attribute_Mapper()
                attribute_object_1.update_object_attributes(temp_dict)
            return attribute_object_1
        elif list_attribute!=None:
            if list_attribute in attribute_dict:
                attribute_object_1=Attribute_Mapper()
                attribute_object_1.update_object_attributes(new_attributes)
                attribute_dict[list_attribute].append(attribute_object_1)
            else:
                attribute_object_1=Attribute_Mapper()
                attribute_object_1.update_object_attributes(new_attributes)
                attribute_dict[list_attribute]=[attribute_object_1]
            attribute_object_2=Attribute_Mapper()
            attribute_object_2.update_object_attributes(attribute_dict)
            return attribute_object_2
        else:
            attribute_dict.update(new_attributes)
            attribute_object_1=Attribute_Mapper()
            attribute_object_1.update_object_attributes(attribute_dict)
            return attribute_object_1

    @classmethod
    def remove_from_list(cls, list1: list, list2: list) -> list:
        """Compares the values between list1 and list2 and appends matching values in a new list which is returned.

        Args:
            list1 (list): The first list.
            list2 (list): The second list.

        Returns:
            list: The list that contains the values which are contained in both lists.
        """
        new_list=[]
        for element in list1:
            if element in list2:
                pass
            else:
                new_list.append(element)
        return new_list

    def get_data_type(self, target_attribute: str, split_target_attribute: str=None, main_target_attribute: str=None) -> Any:
        """Looks up the schema in the object instance to retreive the value of the target attribute provided to the function.

        Args:
            target_attribute (str): The attribute of which the value should be looked up in the schema.
            split_target_attribute (str, optional): The attribute from the end of a string representing a sequence of attributes refering to the schema hierarchy. Defaults to None.
            main_target_attribute (str, optional): In case of a string representing a sequence of attributes, this value represents the original attribute of which value has to be searched in the schema. Defaults to None.

        Returns:
            Any: The value of the attribute in the schema and the attribute.
        """
        
        if "." in target_attribute:
            split_target_attribute=target_attribute.split(".")
            main_target_attribute=split_target_attribute[-1]
            attribute_type=nested_lookup(split_target_attribute[-1], self.schema_skeleton)
        else:
            attribute_type=nested_lookup(target_attribute, self.schema_skeleton)
            main_target_attribute=target_attribute

        if len(attribute_type)>1:
            try:
                split_target_attribute.pop()
                main_target_attribute=target_attribute
                attribute_type, main_target_attribute=self.get_data_type(split_target_attribute[-1], split_target_attribute, main_target_attribute)#check again main attribute target
            except TypeError as e:
                logging.error(f"attribute {attribute_type[0]} occurs multiple times and full path is not provided in the metadata map.")
            except AttributeError as e:
                logging.error(f"attribute {attribute_type[0]} occurs multiple times and full path is not provided in the metadata map.")
        else:
            pass
        if isinstance(attribute_type[0], dict):
            attribute_type=nested_lookup(main_target_attribute, attribute_type[0])
            return attribute_type[0]
        else:
            return attribute_type[0], main_target_attribute

    @classmethod
    def nested_list_level(cls, lst: list) -> int:
        """Returns the nesting level of a list.

        Args:
            lst (list): The nested list.

        Returns:
            int: The level of the list nesting.
        """
        if isinstance(lst, list):
            return 1 + max(cls.nested_list_level(item) for item in lst)
        else:
            return 0

    @classmethod
    def nested_attributes_map_search(cls, attributes_map: dict, target_attribute: str) -> Any:
        """Searches a nested dictionary for a certain target attribute.

        Args:
            attributes_map (dict): The nested dictionary to be searched.
            target_attribute (str): The target attribute in the dictionary.

        Returns:
            Any: The level of the dictionary where the attribute is located at.
        """
        for attribute in attributes_map:
            if (attribute==target_attribute) or target_attribute in attributes_map:
                return attributes_map
            elif isinstance(attributes_map[attribute], Attribute_Mapper):
                return cls.nested_attributes_map_search(attributes_map[attribute].__dict__, target_attribute)
            elif isinstance(attributes_map[attribute], dict):
                return cls.nested_attributes_map_search(attributes_map[attribute], target_attribute)
            else:
                logging.warning(f"{target_attribute} not found in {attributes_map}.")
                pass
        return attributes_map

    @classmethod
    def nested_attributes_map_modification(cls, attributes_map, element_series_attribute):
        for attribute in attributes_map:
            if attribute in element_series_attribute:
                attributes_map[attribute]=element_series_attribute[attribute]
            elif isinstance(attributes_map[attribute], Attribute_Mapper):
                attributes_map[attribute].__dict__.update(cls.nested_attributes_map_modification(attributes_map[attribute].__dict__, element_series_attribute))
                return attributes_map
            elif isinstance(attributes_map[attribute], dict):
                attributes_map[attribute].update(cls.nested_attributes_map_modification(attributes_map[attribute], element_series_attribute))
                return attributes_map
            else:
                logging.warning(f"{element_series_attribute} not found in {attributes_map}.")
                pass
        return attributes_map

    def type_assessment(self, original_attributes_map, map_dict, map_attribute):
        number_of_elements=0
        all_types={}
        for target_attribute in map_dict[map_attribute]:
            attribute_type, target_attribute=self.get_data_type(target_attribute)
            if not target_attribute in original_attributes_map:
                attributes_map=self.nested_attributes_map_search(original_attributes_map, target_attribute)
                if not target_attribute in attributes_map:
                    continue
                else:
                    pass
            else:
                attributes_map=original_attributes_map
            if (isinstance(attributes_map[target_attribute], list)) and (self.nested_list_level(attributes_map[target_attribute]) > self.nested_list_level(attribute_type)):
                number_of_elements=len(attributes_map[target_attribute])
            elif (isinstance(attributes_map[target_attribute], list)) and (self.nested_list_level(attributes_map[target_attribute]) == self.nested_list_level(attribute_type)):
                number_of_elements=1
            else:
                logging.warning(f"no correct type for attribute: {target_attribute}")
            if isinstance(attribute_type, list):
                attribute_type=str(list)
            elif isinstance(attribute_type, dict):
                attribute_type=str(dict)
            elif isinstance(attribute_type, tuple):
                attribute_type=str(dict)
            else:
                pass
            all_types[target_attribute]=attribute_type
        return all_types, number_of_elements