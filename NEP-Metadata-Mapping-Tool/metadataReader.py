import os
from dicomReader import DicomReader
import logging

class MetadataReader:

    #The class is instantiated by providing the path to either a single document that contains the metadata for mapping, or
    #to a folder that contains multiple corresponding files with metadata.
    def __init__(self, metadataDocumentDirectory):
        #Arrays for collected metadata objects in case of multiple dicom files in a folder directory.
        self.allDicomSeries=[]
        isFile = os.path.isfile(metadataDocumentDirectory)
        isDirectory = os.path.isdir(metadataDocumentDirectory)
        if isDirectory==True:
            for i in os.listdir(metadataDocumentDirectory):
                fileName, fileExtension = os.path.splitext(i)
                # If the file in the directory is of dicom format, the dicomReader class is called.
                if fileExtension == ".dcm":
                    f = os.path.join(metadataDocumentDirectory, i)
                    dicomSeries=DicomReader(f, os.path.dirname(metadataDocumentDirectory), fileName)
                    self.allDicomSeries.append(dicomSeries)
                else:
                    logging.warning("File format is not supported.")