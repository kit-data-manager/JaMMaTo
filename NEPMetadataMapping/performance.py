from NEPMetadataMapping.metadataSchemaReader import MetadataSchemaReader
from NEPMetadataMapping.dicomReader import DicomReader
from NEPMetadataMapping.attributeMapping import AttributeMapping
from NEPMetadataMapping.dicomMapping import DicomMapping
from NEPMetadataMapping.mapMRISchema import Map_MRI_Schema

def schema_reader(schema_reader_instance: MetadataSchemaReader) -> None:
    schema_skeleton=schema_reader_instance.json_object_search(schema_reader_instance.schema)

def dicom_reader(dicom_file: str) -> None:
    dicom_object=DicomReader(dicom_file)

def attribute_mapping(dicom_series: DicomReader, map_json_path: str) -> None:
    dicom_mapping=DicomMapping(map_json_path, None, None)
    study_map = AttributeMapping.mapping_from_object(dicom_series.__dict__, dicom_mapping.map_dict, "study")
    series_map = AttributeMapping.mapping_from_object(dicom_series.__dict__, dicom_mapping.map_dict, "series")
    all_attributes_map_list=dicom_mapping.series_extension(dicom_mapping.map_dict, "perImage", dicom_series)
    kwargs={"perImage":all_attributes_map_list}
    series_map.updateMap(**kwargs)
    study_map.updateMap(series=series_map)

def mri_inserter(schema_skeleton: dict, key_list: list, map: object, main_key: str) -> None:
    mri_inserter=Map_MRI_Schema(schema_skeleton, key_list, map, main_key)

def dicom_mapping_class(map_json_path: str, metadata_files_location: str, additional_attributes_list: list) -> None:
    dicom_mapping=DicomMapping(map_json_path, metadata_files_location, additional_attributes_list)
    dicom_mapping.execute_steps(dicom_mapping.map_dict, dicom_mapping.metadata_files_location, dicom_mapping.additional_attributes_list, dicom_mapping.mapped_metadata)