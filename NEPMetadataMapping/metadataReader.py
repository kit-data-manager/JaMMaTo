from distutils import extension
import os
from dicomReader import DicomReader
import logging
import tarfile
import zipfile
import pydicom


class MetadataReader:

    # The class is instantiated by providing the path to either a single document that contains the metadata for mapping, or
    # to a folder that contains multiple corresponding files with metadata.
    def __init__(self, metadataDocumentDirectory):
        # Arrays for collected metadata objects in case of multiple dicom files in a folder directory.
        self.allDicomSeries = []
        isFile = os.path.isfile(metadataDocumentDirectory)
        isDirectory = os.path.isdir(metadataDocumentDirectory)
        if isDirectory == True:
            for i in os.listdir(metadataDocumentDirectory):
                fileName, fileExtension = os.path.splitext(i)
                self.evaluateFileType(i, fileExtension)

        elif isFile == True:
            fileName, fileExtension = os.path.splitext(
                metadataDocumentDirectory)
            #filePath = os.path.dirname(metadataDocumentDirectory)
            match fileExtension:
                case ".zip":
                    with zipfile.ZipFile(metadataDocumentDirectory) as dataset:
                        for i in range(1, len(dataset.filelist)):
                            with dataset.open(dataset.filelist[i].filename) as file:
                                datasetFileName, datasetFileExtension = os.path.splitext(
                                    file.name)
                                self.evaluateFileType(
                                    file, datasetFileExtension)

    def evaluateFileType(self, file, fileExtension):

        # If the file in the directory is of dicom format, the dicomReader class is called.
        if fileExtension == ".dcm":
            try:
                dicomSeries = DicomReader(file)
                self.allDicomSeries.append(dicomSeries)
            except:
                pass
        else:
            logging.error("File format is not supported.")
