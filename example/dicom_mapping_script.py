import sys
from ..NEPMetadataMapping.dicom_mapping import Dicom_Mapping

map_json_path = sys.argv[1]

metadata_files_location = sys.argv[2]

additional_attributes_list = sys.argv[3]

mapped_metadata = sys.argv[4]

Dicom_Mapping(map_json_path, metadata_files_location, additional_attributes_list, mapped_metadata)
