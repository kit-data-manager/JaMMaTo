#This class takes the schema structure as dictionary and the metadata map to assign the metadata values to the schema attributes 
# at the proper hirarchy level.

class MapSchema:

    #This method parses the objects in the schema structure and calls the proper method to insert the attribute value, based on the attribute type.
    def fillObject(self, dictionary: dict(), keys: list(), masterKey: str, values: list()):
        newDict={}
        
        for i in keys:
            if (type(dictionary[i])==type(str()) or type(dictionary[i])==type(tuple())):
                try:
                    for x, y in values[0].__dict__.items():
                        if i==x:
                            newDict[i]=y
                        else: pass
                except(TypeError):
                    #Could be replace with if masterKey in values...
                    for x, y in values.__dict__.items():
                        #Special condition, very specific for the MRI schema, might be changed in a later version
                        if i=="value":
                            if masterKey==x:
                                newDict[i]=self.getType(dictionary[i], y)
                        elif i=="unit":
                            newDict[i]=dictionary[i]
                        elif i==x:
                            newDict[i]=self.getType(dictionary[i], y)
                        else: pass

            elif type(dictionary[i])==type(dict()):
                newDict[i]=self.fillObject(dictionary[i], list(dictionary[i].keys()), i, values)

            elif type(dictionary[i])==type(list()):
                #Special condition, very specific for the MRI schema, might be changed in a later version
                if i=="value":
                    dictionary[masterKey] = dictionary.pop(i)
                    revDict=dict(reversed(list(dictionary.items())))
                    filledArray=self.fillArray(revDict, masterKey, dictionary[masterKey], values)
                else:
                    filledArray=self.fillArray(dictionary, i, dictionary[i], values)
                if len(filledArray)>0:
                    newDict[i]=filledArray
                else: pass
            else: pass
        return newDict

    #This method parses the arrays in the schema structure and calls the proper method to insert the attribute value, based on the attribute type.
    def fillArray(self, jsonObject, jsonObjectProperty, jsonArray, newArrayContent):
        if type(newArrayContent)!=type(list()):
            try:
                for x, y in newArrayContent.__dict__.items():
                    if jsonObjectProperty == x:
                        try:
                            newArrayContent=y
                        except: pass
                    else: pass
            except: #This condition is for the case of having multiple array levels for one attribute, because the logic in the next step expects the value of this key, which is of type string, to recieve a 
                #value of type list.
                if type(newArrayContent)==type(str()):
                    newArrayContent=[newArrayContent]
        elif type(jsonArray[0]) != type(dict()):
            try:
                for x, y in newArrayContent[0].__dict__.items():
                    if jsonObjectProperty == x:
                        try:
                            newArrayContent=y
                        except: pass
                    else: pass
            except: pass
        else: pass
        try:
            jsonArray=jsonArray*len(newArrayContent)
        except Exception as e: pass

        newList=[]

        for i, j in zip(jsonArray, range(0, len(jsonArray))):
            if type(i)==type(str()):
                try:
                    if type(newArrayContent[j])==type(object()):
                        for x, y in newArrayContent[j].__dict__.items():
                            if jsonObjectProperty==x: newList.append(self.getType(type(i), y))
                            else: pass
                    else:
                        newList.append(self.getType(type(i), newArrayContent[j]))
                except: pass
            elif type(i)==type(dict()):
                try:
                    newList.append(self.fillObject(i, list(i.keys()), None, newArrayContent[j]))
                except Exception as e:
                    pass

            elif type(i)==type(list()):
                newList.append(self.fillArray(jsonObject, jsonObjectProperty, i, newArrayContent[j]))
            else: pass
        return newList

    #This method confirms the primitive data types of the attribute values stored in the map and assigns those values to the schema attribute. The correct hirarchial
    #position has been reached through the methods above.
    def getType(self, dataType, variable):
        if dataType=="int":
            return int(variable)
        elif dataType=="float":
            return float(variable)
        else:
            return str(variable)
