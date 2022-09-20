import NEPMetadataMapping.dicomMapping
import sys

map = sys.argv[1]

metadata = sys.argv[2]

mappedMetadata = sys.argv[3]

NEPMetadataMapping.dicomMapping.__init__(map, metadata, mappedMetadata)
