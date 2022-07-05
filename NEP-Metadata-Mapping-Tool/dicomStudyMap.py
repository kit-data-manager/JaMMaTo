#This class contains the hard coded attribute assignments of the dicom metadata values all refering to
# one Study, stored in the DicomReader class instance.

class DicomStudyMap:

    def __init__(self, metadataAttributes):
       for i in metadataAttributes.__dict__:
            if i == "sopClassUid":
                self.studyID=metadataAttributes.__dict__[i]
            if i == "studyDescription":
                self.studyTitle=metadataAttributes.__dict__[i]
            if i == "studyTime":
                self.studyTime=metadataAttributes.__dict__[i]
            if i == "studyDate":
                self.studyDate=metadataAttributes.__dict__[i]
            if i == "softwareVersions":
                self.program=metadataAttributes.__dict__[i]
            if i == "softwareVersions":
                self.program=metadataAttributes.__dict__[i]
            if i == "referringPhysiciansName":
                self.user=metadataAttributes.__dict__[i]
            if i == "institutionName":
                self.institutionName=metadataAttributes.__dict__[i]
            if i == "institutionCodeSequence":
                self.institutionAcronym=metadataAttributes.__dict__[i]
            if i == "institutionalDepartmentName":
                self.institutionDepartment=metadataAttributes.__dict__[i]
            if i == "institutionalDepartmentTypeCodeSequence":
                self.institutionID=metadataAttributes.__dict__[i]
            if i == "personsTelecomInformation":
                self.email=metadataAttributes.__dict__[i]
            if i == "patientsName":
                self.sampleName=metadataAttributes.__dict__[i]
            if i == "patientsID":
                self.sampleID=metadataAttributes.__dict__[i]
            if i == "patientsSize":
                self.sampleID=metadataAttributes.__dict__[i]
            if i == "patientsWeight":
                self.sampleWeight=metadataAttributes.__dict__[i]
            if i == "magneticFieldStrength":
                self.measurementConditions=metadataAttributes.__dict__[i]
            if i == "stationName":
                self.instrumentName=metadataAttributes.__dict__[i]
            if i == "deviceSerialNumber":
                self.instrumentID=metadataAttributes.__dict__[i]
            if i == "manufacturer":
                self.manufacturerName=metadataAttributes.__dict__[i]
            if i == "manufacturersModelName":
                self.modelName=metadataAttributes.__dict__[i]
            if i == "manufacturersDeviceClassUID":
                self.manufacturerID=metadataAttributes.__dict__[i]

            #Additional Attributes, not in the dicom file.
            self.studyName="StudyName"

    #Adding attributes outside of this class, for example the series objects of a study.
    def updateMap(self, **args):
        self.__dict__.update(args)
            