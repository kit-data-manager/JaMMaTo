import sys
from NEPMetadataMapping.dicom_mapping import Dicom_Mapping

map_json_path = sys.argv[1]

metadata_files_location = sys.argv[2]

mapped_metadata = sys.argv[3]

Dicom_Mapping(map_json_path, metadata_files_location, mapped_metadata)
