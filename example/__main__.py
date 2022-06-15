import json
import os
import glob
from MetadataSchemaReader import MetadataSchemaReader
from MetadataReader import MetadataReader
from dicomSeriesMap import dicomSeriesMap
from dicomStudyMap import dicomStudyMap
from fillSchema import fillSchema

jsonSchema = "PATH"
draftDir=glob.glob("PATH")
readSchema=MetadataSchemaReader(jsonSchema, draftDir)
schema=readSchema.searchedSchema
document=MetadataReader("PATH")
metadata=document.allDicomSeries

studyMap=dicomStudyMap(metadata[0])
allSeriesMaps=[]
for i in metadata:
    seriesMap=dicomSeriesMap(i)
    allSeriesMaps.append(seriesMap)
studyMap.updateMap(seriesArray=allSeriesMaps)

fillSchema=fillSchema()
filledSchema=fillSchema.fillObject(schema, list(schema.keys()), studyMap)
print(filledSchema)
