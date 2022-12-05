class AttributeMapping():

    def __init__(self, attributes):
        self.__dict__.update(attributes)

    @classmethod
    def mapping_from_object(cls, metadataAttributes, mapJson, mapObject):
        temp={}
        for i, j in mapJson[mapObject].items():
            if i in metadataAttributes:
                temp[j]= metadataAttributes[i]
            else:
                pass
        return cls(temp)

    def updateMap(self, **kwargs):
        self.__dict__.update(kwargs)
