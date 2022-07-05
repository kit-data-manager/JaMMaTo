#Extends on dicomStudyMap with the schema attributes that have different values for each dicom Series of a Study. Therefore, each Series (i.e. dicom file) has one
#class instance.

class DicomSeriesMap:

    def __init__(self, metadataAttributes):

        for i in metadataAttributes.__dict__:
            if i == "seriesID":
                    self.seriesID=metadataAttributes.__dict__[i]
            if i == "seriesDescription":
                self.seriesTitle=metadataAttributes.__dict__[i]
            if i == "ProtocolName":
                self.sequenceProtocol=metadataAttributes.__dict__[i]
            if i == "effectiveEchoTime":
                self.effectiveEchoTime=metadataAttributes.__dict__[i]
            if i == "repetitionTime":
                self.repetitionTime=metadataAttributes.__dict__[i]
            if i == "flipAngle":
                self.flipAngle=metadataAttributes.__dict__[i]
            if i == "numberOfFrames":
                self.numberOfImages=metadataAttributes.__dict__[i]
            if i == "imageOrientation":
                self.imageOrientation=metadataAttributes.__dict__[i]
            if i == "pixelSpacing":
                self.pixelSpacing=metadataAttributes.__dict__[i]
            if i == "sliceThickness":
                self.sliceThickness=metadataAttributes.__dict__[i]
            if i == "imageSize":
                self.imageSize=metadataAttributes.__dict__[i]
            if i == "rows":
                self.rows=metadataAttributes.__dict__[i]
            if i == "columns":
                self.columns=metadataAttributes.__dict__[i]
            if i == "frameType":
                self.imageType=metadataAttributes.__dict__[i]
            if i == "imagePosition":
                self.sampleImagePosition=metadataAttributes.__dict__[i]
            if i == "pixelRepresentation":
                self.pixelRepresentation=metadataAttributes.__dict__[i]
            if i == "smallestImagePixelValue":
                self.smallestImagePixelValue=metadataAttributes.__dict__[i]
            if i == "largestImagePixelValue":
                self.largestImagePixelValue=metadataAttributes.__dict__[i]
            if i == "pixelBandwidth":
                self.pixelBandwidth=metadataAttributes.__dict__[i]
