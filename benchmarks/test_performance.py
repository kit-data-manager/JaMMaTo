from NEPMetadataMapping.metadataSchemaReader import MetadataSchemaReader
from NEPMetadataMapping.dicomReader import DicomReader
from NEPMetadataMapping.attributeMapping import AttributeMapping
from NEPMetadataMapping.dicomMapping import DicomMapping
from NEPMetadataMapping.performance import dicom_mapping_class, dicom_mapping_class, schema_reader, dicom_reader, attribute_mapping, mri_inserter
from typing import Any
import json

NUM_ROUNDS=10
NUM_ITERATIONS=100

schema_path = open("/Users/nicoblum/bwSyncShare/VSCode/NEPMappingTool/NEP-Metadata-Mapping-Tool/schemas/mriSchmemaV2_1.json")
jsonSchema = json.load(schema_path)
schema_reader_instance=MetadataSchemaReader(jsonSchema)
schema_skeleton=schema_reader_instance.json_object_search(schema_reader_instance.schema)
dicom_file="/Users/nicoblum/bwSyncShare/NEP/DicomTestStudy/Series/series7.dcm"
dicom_object=DicomReader(dicom_file)
map_json_path="/Users/nicoblum/bwSyncShare/map.json"
dicom_mapping=DicomMapping(map_json_path, None, None)
study_map = AttributeMapping.mapping_from_object(dicom_object.__dict__, dicom_mapping.map_dict, "study")
series_map = AttributeMapping.mapping_from_object(dicom_object.__dict__, dicom_mapping.map_dict, "series")
all_attributes_map_list=dicom_mapping.series_extension(dicom_mapping.map_dict, "perImage", dicom_object)
kwargs={"perImage":all_attributes_map_list}
series_map.updateMap(**kwargs)
study_map.updateMap(series=series_map)
dicom_file_zipped="/Users/nicoblum/bwSyncShare/NEP/DicomTestStudy/small.zip"

def test_schema_reader(benchmark: Any) -> None:
    benchmark.pedantic(
        schema_reader,
        args=(schema_reader_instance,),
        rounds=NUM_ROUNDS,
        iterations=NUM_ITERATIONS
    )
def test_dicom_reader(benchmark: Any) -> None:
    benchmark.pedantic(
        dicom_reader,
        args=(dicom_file,),
        rounds=NUM_ROUNDS,
        iterations=NUM_ITERATIONS
    )
def test_attribute_mapping(benchmark: Any) -> None:
    benchmark.pedantic(
        attribute_mapping,
        args=(dicom_object, map_json_path),
        rounds=NUM_ROUNDS,
        iterations=NUM_ITERATIONS
    )
def test_mri_inserter(benchmark: Any) -> None:
    benchmark.pedantic(
        mri_inserter,
        args=(schema_skeleton, list(schema_skeleton.keys()), study_map, None),
        rounds=NUM_ROUNDS,
        iterations=NUM_ITERATIONS
    )
def test_dicom_mapping(benchmark: Any) -> None:
    benchmark.pedantic(
        dicom_mapping_class,
        args=(map_json_path, dicom_file_zipped, ["perImage"]),
        rounds=NUM_ROUNDS,
        iterations=NUM_ITERATIONS
    )