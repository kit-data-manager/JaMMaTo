import json
from metadataSchemaReader import MetadataSchemaReader
from metadataReader import MetadataReader
from dicomStudyMap import DicomStudyMap
from dicomSeriesMap import DicomSeriesMap
from mapSchema import MapSchema

#This class uses all components of the mapping tool functionality for dicom and executes them consecutively in the proper order. 
class DicomMapping:

    def __init__(self, jsonSchema, metadata, draftDir=None, mappedMetadata='mappedMetadata.json'):
        
        #The first class reads in the schema and the json rafts for validating the schema for versioning. 
        readSchema=MetadataSchemaReader(jsonSchema, draftDir)
        #This class attribute contains the schema structure in the Python-based environment.
        schema=readSchema.searchedSchema
        #The second class that reads in the dicom files, which beling to one MRI series. Takes the directory as argument.
        document=MetadataReader(metadata)
        #This class attribute is a list of all 
        metadata=document.allDicomSeries

        #The third class instantiates the map for one MRI study, by taking one arbitrary object class of the list that contains all dicom files.
        studyMap=DicomStudyMap(metadata[0])

        #The studyMap contains all schema attributes with their values from the MRI study.
        #The fourth class instantiates the maps for all series within the MRI study, one class instance per dicom file.
        allSeriesMaps=[]
        for i in metadata:
            seriesMap=DicomSeriesMap(i)
            allSeriesMaps.append(seriesMap)

        #This function updates the map for the MRI study, by adding the list containing all series classes.
        #The studyMap now contains also all series object classes with the schema attributes and their values from each dicom file of a series belonging to the study.
        studyMap.updateMap(series=allSeriesMaps)

        #The fith class takes the schema structure and the schema attributes from the first hirarchy, and the studyMap class with the attributes and their values. It then fills the schema structure with the attribute values, 
        #according to their position in the schema.
        filledSchema=MapSchema()
        filledSchema=filledSchema.fillObject(schema, list(schema.keys()), studyMap)
        #The filled schema is then written to a json document and saved.
        with open(mappedMetadata, 'w') as f:
            json.dump(filledSchema, f)