import json
import logging
import os
from jsonschema import validate
import glob

class MetadataSchemaReader():

    def __init__(self, schema, draftDir):
        draftDirFiles=glob.glob(draftDir)
        fileName, fileExtension = os.path.splitext(schema)
        if fileExtension == ".json":
            jsonSchema=open(schema)
            jsonSchema = json.load(jsonSchema)
            try:
                self.definitions=jsonSchema["definitions"]
            except:
                pass
            self.jsonSchemaValidator(jsonSchema, draftDirFiles)
            self.searchedSchema=self.jsonObjectsearch(jsonSchema)
        else:
            logging.warning("Schema format not supported.")
            
    def jsonSchemaValidator(self, jsonSchema, draftDirFiles):
        #Validation of the file read in is of proper JSON Format, corresponding to the latest draft supported by this application or earlier
        for i in draftDirFiles:    
            j=json.load(open(i))
            try:
                validate(instance=jsonSchema, schema=j)
                logging.info("Schema is valid for draft: %s", str(i))
                break
            except Exception as e:
                logging.warning("Schema is not valid")
                pass

    def jsonDefinitionSearch(self, definition):
        properties=None
        if "$ref" in definition:
            if definition["$ref"].startswith("#"):
                keyword=definition[1]["$ref"].split("/")[-1:][0]
                subProperties=self.jsonDefinitionSearch(self.definitions[keyword])
                properties[definition]=[subProperties]
            else:
                path=definition["$ref"].split("#")[0]
                print(path)
        elif definition["type"] == "array":
            subProperties=self.jsonArraySearch(definition)
            properties=subProperties
        elif definition["type"] == "object":
            subProperties=self.jsonObjectsearch(definition)
            properties=subProperties
        else:
            properties=self.jsonTypeSearch(definition["type"])
        return properties

    def jsonArraySearch(self, property):
        subProperties=None
        if "$ref" in property["items"]:
            if property["items"]["$ref"].startswith("#"):
                keyword=property["items"]["$ref"].split("/")[-1:][0]
                subProperties=self.jsonDefinitionSearch(self.definitions[keyword])
            else:
                path=property["items"]["$ref"].split("#")[0]
                print(path)
        elif "oneOf" in property["items"]:
            for i in property["items"]["oneOf"]:
                if "$ref" in i:
                    if i["$ref"].startswith("#"):
                        keyword=i["$ref"].split("/")[-1:][0]
                        subProperties=self.jsonDefinitionSearch(self.definitions[keyword])
                    else:
                        path=i["$ref"].split("#")[0]
        elif property["items"]["type"] == "array":
            subProperties=[self.jsonArraySearch(property["items"])]
        elif property["items"]["type"] == "object":
            subProperties=self.jsonObjectsearch(property["items"])
        else:
            subProperties=self.jsonTypeSearch(property["items"]["type"])
        return subProperties

    def jsonObjectsearch(self, property):
        properties={}
        for i in property["properties"].items():
            if "$ref" in i[1]:
                if i[1]["$ref"].startswith("#"):
                    keyword=i[1]["$ref"].split("/")[-1:][0]
                    subProperties=self.jsonDefinitionSearch(self.definitions[keyword])
                    properties[i[0]]=[subProperties]
                else:
                    path=i[1]["$ref"].split("#")[0]
                    print(path)
            elif i[1]["type"] == "array":
                subProperties=self.jsonArraySearch(i[1])
                properties[i[0]]=[subProperties]
            elif i[1]["type"] == "object":
                subProperties=self.jsonObjectsearch(i[1])
                properties[i[0]]=subProperties
            else:
                if i[0] == "value":
                    properties[i[0]]=self.jsonTypeSearch(i[1]["type"])
                elif i[0] == "unit":
                    properties[i[0]]=i[1]["default"]
                else:
                    properties[i[0]]=self.jsonTypeSearch(i[1]["type"])
        return properties

    def jsonTypeSearch(self, type):
        if type=="integer":
            return "int"
        elif type=="string":
            return "str"
        elif type=="number":
           return "float"
        elif type=="boolean":
           return "bool"
        elif type=="null":
            return None
        elif isinstance(type, list):
            multipleTypes=[]
            for j in type:
                multipleTypes.append(self.jsonTypeSearch(j))
            return tuple(multipleTypes)
        else:
            print(TypeError)
