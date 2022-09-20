import sys
sys.path.append('../NEPMetadataMapping')
import dicomMapping

map = sys.argv[1]

metadata = sys.argv[2]

mappedMetadata = sys.argv[3]

dicomMapping.DicomMapping(map, metadata, mappedMetadata)
