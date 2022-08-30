import pandas as pd

class ExcelIngest:

    def __init__(self, metadataAttributes, excelSheetPath, sheetName):
        excelDataFrame=pd.read_excel(open(excelSheetPath, 'rb'), 
            sheet_name=sheetName, header=None)
       
        for x in range(0, len(excelDataFrame[0])):
            if excelDataFrame[0][x] in metadataAttributes.__dict__:

                temp={excelDataFrame[1][x]: metadataAttributes.__dict__[excelDataFrame[0][x]]}
                self.__dict__.update(temp)
    
    def updateMap(self, **args):
        self.__dict__.update(args)
        
