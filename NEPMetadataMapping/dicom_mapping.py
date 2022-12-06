import json
from .schema_reader import Schema_Reader
from .metadata_reader import Metadata_Reader
from .map_mri_schema import Map_MRI_Schema
from .attribute_mapping import Attribute_Mapping
from .dicom_reader import Dicom_Reader
from .cache_schemas import Cache_Schemas

class Dicom_Mapping():
    
    def __init__(self, map_json_path: str, metadata_files_location: str, additional_attributes_list: list, mapped_metadata: str='mapped_metadata.json') -> None:
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
        self.additional_attributes_list=additional_attributes_list
        self.mapped_metadata=mapped_metadata
        self.execute_steps(map_dict, metadata_files_location, additional_attributes_list, mapped_metadata)

    def execute_steps(self, map_dict: dict, metadata_files_location: str, additional_attributes_list: list, mapped_metadata: str) -> None:
        """Executes all steps for mapping a dicom study to a json schema.

        Args:
            map_dict (dict): The map of the attribute assignments for mapping as a dictionary.
            metadata_files_location (str): The directory where the dicom files of a study are stored.
            mapped_metadata (str): The resulting json file.
        """

        json_schema = Cache_Schemas.cache_schema(map_dict).json_schema
        schema_skeleton = Schema_Reader(json_schema)
        schema_skeleton = schema_skeleton.json_object_search(schema_skeleton.schema)
        dicom_object = Metadata_Reader(metadata_files_location)
        self.validate_study(dicom_object)
        dicom_series_list = dicom_object.all_dicom_series

        study_map = Attribute_Mapping.mapping_from_object(dicom_series_list[0].__dict__, map_dict, "study")
        series_maps_list = []
        for series in dicom_series_list:
            series_map = Attribute_Mapping.mapping_from_object(series.__dict__, map_dict, "series")
            for additional_attributes in additional_attributes_list:
                all_attributes_map_list=self.series_extension(map_dict, additional_attributes, series)
                kwargs={f"{additional_attributes}":all_attributes_map_list}
                series_map.update_map(**kwargs)
            series_maps_list.append(series_map)
        study_map.update_map(series=series_maps_list)
        
        map_mri_schema = Map_MRI_Schema(schema_skeleton, list(schema_skeleton.keys()), study_map, None)
        filled_schema = map_mri_schema.fill_json_object(map_mri_schema.schema_skeleton, map_mri_schema.key_list, map_mri_schema.map, map_mri_schema.main_key)
        with open(mapped_metadata, 'w') as f:
            json.dump(filled_schema, f)

    def validate_study(self, dicom_object: Metadata_Reader) -> None:
        """Validate that all dicom files (series) of a study have the same Study Instance UID.

        Args:
            dicom_object (MetadataReader): The object that contains the dicom metadata attributes.

        Raises:
            Exception: Strings are not the same.
        """
        allStudyInstanceUIDs = []
        for series in dicom_object.all_dicom_series:
            allStudyInstanceUIDs.append(series.studyInstanceUid)

        if all(series == allStudyInstanceUIDs[0] for series in allStudyInstanceUIDs) == True:
            pass
        else:
            raise Exception('Files are not from the same study.')

    def series_extension(self, map_dict: dict, map_attribute: str, series: Dicom_Reader) -> list:
        """Extends the mapped attributes of a series object by an attribute that has a list of objects as values, using the keywords of the provided map.

        Args:
            map_dict (dict): Map that contains the attribute assignments for the dicom metadata and the schema.
            map_attribute (str): The attribute in the map that contains the mapping assignments.
            series (DicomReader): The series which is extended.

        Returns:
            list: A list of objects with the mapped attributes.
        """
        all_attributes_map_list=[]
        numer_of_sub_attributes=len(map_dict[map_attribute])
        number_of_additional_objects=len(series.__dict__[list(map_dict[map_attribute].keys())[0]])
        
        for object_number in range(0, number_of_additional_objects):
            temp_image_attributes={}
            for attribute_number in range(0, numer_of_sub_attributes):
                temp_image_attributes[list(map_dict[map_attribute].keys())[attribute_number]]=series.__dict__[list(map_dict[map_attribute].keys())[attribute_number]][object_number]
            attributes_map = Attribute_Mapping.mapping_from_object(temp_image_attributes, map_dict, map_attribute)
            all_attributes_map_list.append(attributes_map)
        return all_attributes_map_list

Dicom_Mapping("example/map.json", "/Users/nicoblum/bwSyncShare/NEP/DicomTestStudy/Series/small/Archiv.zip", ["perImage"])