import pydicom
import re
import logging
from datetime import datetime

# This class instantiates the class object of a dicom file, which contains the key-value pairs of the fiel metadata.
class DicomReader:
    
    def __init__(self, dicomFile, studyName, seriesName):
        
        try:
            self.dicomFile=pydicom.dcmread(dicomFile)
        except Exception as e:
            logging.warning("Error for file: %s %s", dicomFile, e)
            self.dicomFile=pydicom.dcmread(dicomFile, force=True)
        
        self.studyName=studyName
        self.seriesName=seriesName
        self.studyDateTime=None
        self.mainDict={}
        self.subDict=self.pydicomObjects(self.dicomFile)
        self.__dict__.update(self.mainDict)
        self.studyDateTime =  datetime.strptime(self.studyDateTime, '%Y%m%d %H%M%S').isoformat()
        self.__dict__.pop("mainDict")
        self.__dict__.pop("subDict")
        self.__dict__.pop("dicomFile")
        self.__dict__.pop("pixelData")
        #print(self.__dict__)
    #This method parses the pydicom.Dataset and pydicom.Sequence objects created by the pyDicom module to retrieve the primitive data types
    # and separate the attributes.
    def pydicomObjects(self, dataset):
        subDict={}
        subList=[]
        for i in dataset:
            if isinstance(i, pydicom.Dataset):
                subList.append(self.pydicomObjects(i))
            elif isinstance(i.value, pydicom.Sequence):
                name=i.name.split()
                if len(name)==1:
                    name=name[0].lower()
                else:
                    subname=""
                    for j in name[1:]:
                        subname+=j.capitalize()

                    name=name[0].lower() + subname

                name=re.sub('[^A-Za-z0-9]+', '', name)
                subDict[name]=self.pydicomObjects(i.value)
            else:
                name=i.name.split()
                if len(name)==1:
                    name=name[0].lower()
                else:
                    subname=""
                    for j in name[1:]:
                        subname+=j.capitalize()

                    name=name[0].lower() + subname

                name=re.sub('[^A-Za-z0-9]+', '', name)
                if name == "studyDate":
                    self.studyDateTime=i.value+" "
                if name == "studyTime":
                    self.studyDateTime += i.value
                subDict[name]=i.value
                self.mainDict[name]=i.value

        if len(subList)>0:
            return subList
        else:
            return subDict