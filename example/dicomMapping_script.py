import sys
sys.path.append('../NEPMetadataMapping')
map = sys.argv[1]
import dicomMapping

metadata = sys.argv[2]

mappedMetadata = sys.argv[3]

dicomMapping.DicomMapping(map, metadata, mappedMetadata)
