import json


class AttributeMapping():

    def __init__(self, metadataAttributes, mapJson, mapObject):

        for i, j in mapJson[mapObject].items():
            if i in metadataAttributes.__dict__:
                temp = {j: metadataAttributes.__dict__[i]}
                self.__dict__.update(temp)

    def updateMap(self, **args):
        self.__dict__.update(args)
