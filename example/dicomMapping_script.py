import dicomMapping
import sys

metadata = sys.argv[1]

map = sys.argv[2]

mappedMetadata = sys.argv[3]

dicomMapping.__init__(metadata, map, mappedMetadata)
