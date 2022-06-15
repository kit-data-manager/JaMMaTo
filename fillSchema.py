class fillSchema:

    def fillObject(self, dictionary: dict(), keys: list(), values: list()):
        newDict={}
        for i in keys:
            if (type(dictionary[i])==type(str()) or type(dictionary[i])==type(tuple())):
                try:
                    for x, y in values[0].__dict__.items():
                        if i==x:
                            newDict[i]=y
                        else: pass
                except(TypeError):
                    for x, y in values.__dict__.items():
                        if i==x:
                            newDict[i]=self.getType(dictionary[i], y)
                        else: pass

            elif type(dictionary[i])==type(dict()):
                newDict[i]=self.fillObject(dictionary[i], list(dictionary[i].keys()), values)

            elif type(dictionary[i])==type(list()):
                filledArray=self.fillArray(dictionary, i, dictionary[i], values)
                if len(filledArray)>0:
                    newDict[i]=filledArray
                else: pass
            else: pass
        return newDict

    def fillArray(self, jsonObject, jsonObjectProperty, jsonArray, newArrayContent):
        if type(newArrayContent)!=type(list()):
            try:
                for x, y in newArrayContent.__dict__.items():
                    if jsonObjectProperty == x:
                        try:
                            newArrayContent=y
                        except:
                            pass
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
                        except:
                            pass
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
                except:
                    pass
            elif type(i)==type(dict()):
                try:
                    newList.append(self.fillObject(i, list(i.keys()), newArrayContent[j]))
                except Exception as e:
                    pass

            elif type(i)==type(list()):
                newList.append(self.fillArray(jsonObject, jsonObjectProperty, i, newArrayContent[j]))
            else:
                pass
        return newList

    def getType(self, type, variable):
        if type=="str":
            return str(variable)
        elif type=="int":
            return int(variable)
        elif type=="float":
            return float(variable)
        else:
            return str(variable)