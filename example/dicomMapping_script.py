import NEPMetadataMapping.dicomMapping
import sys

metadata = sys.argv[1]

map = sys.argv[2]

mappedMetadata = sys.argv[3]

NEPMetadataMapping.dicomMapping.__init__(metadata, map, mappedMetadata)
