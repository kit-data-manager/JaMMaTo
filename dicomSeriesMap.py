#depends on dicomStudyMap

class dicomSeriesMap:

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
                self.frameType=metadataAttributes.__dict__[i]
            if i == "sampleImagePosition":
                self.sampleImagePosition=metadataAttributes.__dict__[i]
            if i == "pixelPresentation":
                self.pixelPresentation=metadataAttributes.__dict__[i]
            if i == "smallestImagePixelValue":
                self.smallestImagePixelValue=metadataAttributes.__dict__[i]
            if i == "largestImagePixelValue":
                self.largestImagePixelValue=metadataAttributes.__dict__[i]
            if i == "pixelBandwidth":
                self.pixelBandwidth=metadataAttributes.__dict__[i]
