import os
from dicomReader import dicomReader
import logging

class MetadataReader:

    #The class is instantiated by providing the path to either a single document that contains the metadata for mapping, or
    #to a folder that contains multiple corresponding files with metadata.
    def __init__(self, metadataDocumentDirectory):
        #Arrays for collected metadata objects in case of a multiple files in a folder directory
        self.allDicomSeries=[]
        isFile = os.path.isfile(metadataDocumentDirectory)
        isDirectory = os.path.isdir(metadataDocumentDirectory)
        if isDirectory==True:
            for i in os.listdir(metadataDocumentDirectory):
                fileName, fileExtension = os.path.splitext(i)
                if fileExtension == ".dcm":
                    f = os.path.join(metadataDocumentDirectory, i)
                    seriesName=i
                    dicomSeries=dicomReader(f, os.path.dirname(metadataDocumentDirectory), seriesName)
                    self.allDicomSeries.append(dicomSeries)
                else:
                    logging.warning("File format is not supported.")