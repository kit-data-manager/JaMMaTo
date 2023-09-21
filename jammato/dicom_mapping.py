import json
import os
import logging
from .schema_reader import Schema_Reader
from .dicom_reader import Dicom_Reader
from .cache_schemas import Cache_Schemas
from .analyse_study import Analyse_Study
from .data_cleaning import data_cleaning_instance
from .metadata_reader import Metadata_Reader
from .attribute_mapper import Attribute_Mapper
from .attribute_inserter import Attribute_Inserter

class Dicom_Mapping():
    
    def __init__(self, map_json_path: str, metadata_files_location: str, mapped_metadata: str='mapped_metadata.json', config_dicom_file_validation: str=os.getcwd()+"/configs/config_dicom_file_validation.json") -> None:
        """Instantiates the class, loads the map dictionary from JSON, instantiates all attributes to the object and executes the steps for mapping.

        Args:
            map_json (json): A json based map of the attribute assignments for mapping.
            metadata_files_location (str): The directory where the dicom files of a study are stored.
            mapped_metadata (str, optional): The resulting json file. Defaults to 'mapped_metadata.json'.
        """
        with open(map_json_path, 'r') as f:
            map_dict = json.load(f)
        self.map_dict=map_dict
        self.metadata_files_location = metadata_files_location
        self.mapped_metadata=mapped_metadata
        self.config_dicom_file_validation=config_dicom_file_validation
        self.analyse_study_instance=Analyse_Study(config_dicom_file_validation)
        data_cleaning_instance
        self.execute_steps(map_dict, metadata_files_location, mapped_metadata)

    def execute_steps(self, map_dict: dict, metadata_files_location: str, mapped_metadata: str) -> None:
        """Executes all steps for mapping a dicom study to a json schema, i.e. download or cache the target schema, extract the schema skeleton, read the metadata from the DICOM files and extract metadata,
        map the attributes provided in the JSON metadata map, create the mapped metadata object, fill the schema skeleton with the attributes in the mapped metadata object and finally store the result as JSON document.

        Args:
            map_dict (dict): The map of the attribute assignments for mapping as a dictionary.
            metadata_files_location (str): The directory where the dicom files of a study are stored.
            mapped_metadata (str): The resulting json file.
        """
        json_schema = Cache_Schemas.cache_schema(map_dict).json_schema
        schema_skeleton = Schema_Reader(json_schema)
        self.schema_skeleton = schema_skeleton.json_object_search(schema_skeleton.schema)
        dicom_object = Metadata_Reader(metadata_files_location, self.config_dicom_file_validation)
        dicom_series_list = dicom_object.all_dicom_series
        study_map = Attribute_Mapper.mapping_from_object(dicom_series_list[0].__dict__, map_dict, list(map_dict.keys())[1], [])
        if len(list(map_dict.keys())) > 2:
            merged_series_dict=self.map_and_merge_series(dicom_series_list, map_dict)
            for merged_series in merged_series_dict.values():

                if list(map_dict.keys())[1] in study_map:
                    merged_study_map=Attribute_Mapper.merge_mapped_attributes(study_map[list(map_dict.keys())[1]], merged_series, list(map_dict.keys())[2])
                else:
                    merged_study_map=Attribute_Mapper.merge_mapped_attributes(study_map, merged_series, list(map_dict.keys())[2])
            merged_study_map={list(map_dict.keys())[1]: merged_study_map}
        else:
            pass
        
        map_schema = Attribute_Inserter(self.schema_skeleton, list(self.schema_skeleton.keys()), merged_study_map)
        filled_schema = map_schema.fill_json_object(map_schema.schema_skeleton, map_schema.key_list, map_schema.map)
        with open(mapped_metadata, 'w') as f:
            json.dump(filled_schema, f)

        return

    def map_and_merge_series(self, dicom_series_list: list, map_dict: dict) -> dict:
        """Mapping and merging of the series that are part of a MRI study.

        Args:
            dicom_series_list (list): The list of metadata objects from the metadata extraction of the DICOM files.
            map_dict (dict): The JSON map that contains the attribute assignments of the origin and target attributes.

        Returns:
            dict: The dictionary that contains the mapped and merged metadata attributes.
        """
        merged_series_dict={}
        if len(list(map_dict.keys())) == 4:
            for raw_series in dicom_series_list:
                duplicate_sop_elements, duplicate_series_elements=self.analyse_study_instance.analyse_study(raw_series)
                if (duplicate_sop_elements==False) and (duplicate_series_elements==True):
                    series_map={list(map_dict.keys())[2]: self.analyse_study_instance.get_series(raw_series.__dict__[self.analyse_study_instance.file_series_instance_uid])}####
                    merged_series_map=self.series_extension(map_dict, list(map_dict.keys())[3], raw_series, series_map)
                elif (duplicate_sop_elements==True) and (duplicate_series_elements==True):
                    merged_series_map=Attribute_Mapper()
                    pass
                else:
                    series_map = Attribute_Mapper.mapping_from_object(raw_series.__dict__, map_dict, list(map_dict.keys())[2], [list(map_dict.keys())[1]])
                    merged_series_map=self.series_extension(map_dict, list(map_dict.keys())[3], raw_series, series_map)
                    self.analyse_study_instance.set_series(raw_series.__dict__[self.analyse_study_instance.file_series_instance_uid], merged_series_map)
                merged_series_dict[raw_series.__dict__[self.analyse_study_instance.file_series_instance_uid]]=merged_series_map 
        else:
            for raw_series in dicom_series_list:
                duplicate_sop_elements, duplicate_series_elements=self.analyse_study_instance.analyse_study(raw_series)
                if (duplicate_sop_elements==True) and (duplicate_series_elements==True):
                    series_map=Attribute_Mapper()
                    pass
                else:
                    series_map = Attribute_Mapper.mapping_from_object(raw_series.__dict__, map_dict, list(map_dict.keys())[2], [list(map_dict.keys())[1]])
                    self.analyse_study_instance.set_series(raw_series.__dict__[self.analyse_study_instance.file_series_instance_uid], series_map)
                merged_series_dict[raw_series.__dict__[self.analyse_study_instance.file_series_instance_uid]]=series_map

        return merged_series_dict

    def series_extension(self, map_dict: dict, map_attribute: str, series: Dicom_Reader, series_map) -> list:
        """Extends the mapped attributes of a series object by an attribute that has a list of objects as values, using the keywords of the provided map.

        Args:
            map_dict (dict): Map that contains the attribute assignments for the dicom metadata and the schema.
            map_attribute (str): The attribute in the map that contains the mapping assignments.
            series (DicomReader): The series which is extended.

        Returns:
            list: A list of objects with the mapped attributes.
        """
        attribute_value=None
        target_attributes={}
        for origin_attribute in list(map_dict[map_attribute].values()):
            try:
                attribute_value=series.__dict__[origin_attribute]
            except KeyError as e:
                continue
            target_attributes[origin_attribute]=attribute_value
        attributes_map = Attribute_Mapper.mapping_from_object(target_attributes, map_dict, map_attribute, [list(map_dict.keys())[1], list(map_dict.keys())[2]])

        assess_type=Attribute_Mapper(**{"schema_skeleton": self.schema_skeleton})
        all_types, number_of_elements=assess_type.type_assessment(attributes_map, map_dict, map_attribute)

        for key in all_types:
            new_attributes_map={}
            if not key in attributes_map:
                new_attributes_map.update(assess_type.nested_attributes_map_search(attributes_map, key))
            else:
                pass

        if len(new_attributes_map) > 0:
            pass
        else:
            new_attributes_map=attributes_map

        for element in range(0, number_of_elements):
            element_series_attribute={}

            for series_attribute, attribute_value in new_attributes_map.items():
                if (isinstance(attribute_value, list)) and (((isinstance(attribute_value[0], list)) and (str(type(attribute_value[0]))== all_types[series_attribute])) or ((isinstance(attribute_value[0], list))==False) and (str(type(attribute_value[0])) == all_types[series_attribute])):    
                    element_series_attribute[series_attribute]=attribute_value[element]

                elif isinstance(attribute_value, list) == False:
                    element_series_attribute[series_attribute]=element_series_attribute[series_attribute]=attribute_value

                elif (isinstance(attribute_value, list)) and (str(type(attribute_value)) == all_types[series_attribute]):
                    element_series_attribute[series_attribute]=element_series_attribute[series_attribute]=attribute_value
                    
                else:
                    logging.error(f"The value for attribute {series_attribute} does not correspond to the required value in the schema.")

            if set(element_series_attribute.keys()).issubset(set(attributes_map.keys())):
                pass
            else:
                element_series_attribute=assess_type.nested_attributes_map_modification(attributes_map, element_series_attribute)

            if list(map_dict.keys())[2] in series_map:
                merged_series_map=assess_type.merge_mapped_attributes(series_map[list(map_dict.keys())[2]], element_series_attribute, list(map_dict.keys())[3])
            else:
                merged_series_map=assess_type.merge_mapped_attributes(series_map, element_series_attribute, list(map_dict.keys())[3])

        return merged_series_map    