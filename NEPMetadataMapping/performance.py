from .schema_reader import Schema_Reader
from .dicom_reader import Dicom_Reader
from .attribute_mapping import Attribute_Mapping
from .dicom_mapping import Dicom_Mapping
from .map_mri_schema import Map_MRI_Schema

def schema_reader(schema_reader_instance: Schema_Reader) -> None:
    schema_skeleton=schema_reader_instance.json_object_search(schema_reader_instance.schema)

def dicom_reader(dicom_file: str) -> None:
    dicom_object=Dicom_Reader(dicom_file)

def attribute_mapping(dicom_series: Dicom_Reader, map_json_path: str) -> None:
    dicom_mapping=Dicom_Mapping(map_json_path, None, None)
    study_map = Attribute_Mapping.mapping_from_object(dicom_series.__dict__, dicom_mapping.map_dict, "study")
    series_map = Attribute_Mapping.mapping_from_object(dicom_series.__dict__, dicom_mapping.map_dict, "series")
    all_attributes_map_list=dicom_mapping.series_extension(dicom_mapping.map_dict, "perImage", dicom_series)
    kwargs={"perImage":all_attributes_map_list}
    series_map.update_map(**kwargs)
    study_map.update_map(series=series_map)

def mri_inserter(schema_skeleton: dict, key_list: list, map: object, main_key: str) -> None:
    mri_inserter=Map_MRI_Schema(schema_skeleton, key_list, map, main_key)

def dicom_mapping_class(map_json_path: str, metadata_files_location: str, additional_attributes_list: list) -> None:
    dicom_mapping=Dicom_Mapping(map_json_path, metadata_files_location, additional_attributes_list)
    dicom_mapping.execute_steps(dicom_mapping.map_dict, dicom_mapping.metadata_files_location, dicom_mapping.additional_attributes_list, dicom_mapping.mapped_metadata)