from matplotlib.font_manager import json_dump
import pydicom
import re
import logging

class dicomReader:
    
    def __init__(self, dicomFile, studyName, seriesName):
        
        try:
            self.dicomFile=pydicom.dcmread(dicomFile)
        except Exception as e:
            logging.warning("Error for file: %s %s", dicomFile, e)
            self.dicomFile=pydicom.dcmread(dicomFile, force=True)
        
        self.studyName=studyName
        self.seriesName=seriesName
        self.mainDict={}
        self.subDict=self.dataset(self.dicomFile)
        self.__dict__.update(self.mainDict)
        self.__dict__.pop("mainDict")
        self.__dict__.pop("subDict")
        self.__dict__.pop("dicomFile")
        self.__dict__.pop("pixelData")

    def dataset(self, dataset):
        subDict={}
        subList=[]
        for i in dataset:
            if isinstance(i, pydicom.Dataset):
                subList.append(self.dataset(i))
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
                subDict[name]=self.sequence(i.value)
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
               
                subDict[name]=i.value
                self.mainDict[name]=i.value

        if len(subList)>0:
            return subList
        else:
            return subDict

    def sequence(self, sequence):
        subDict={}
        subList=[]
        for i in sequence:
            if isinstance(i, pydicom.Dataset):
                subList.append(self.dataset(i))
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
                subDict[name]=self.sequence(i.value)
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
                subDict[name]=i.value
                self.mainDict[name]=i.value

        if len(subList)>0:
            return subList
        else:
            return subDict