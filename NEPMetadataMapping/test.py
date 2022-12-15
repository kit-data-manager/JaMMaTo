import time

t1 = time.time()
nums = range(100000000)
sum = 0
for k in nums:
    sum = sum + k
print("Sum of 1,000 numbers is : ", sum)
t2 = time.time()
t = t2 - t1
print("Elapsed time is : ", t, " seconds")

#Dicom_Mapping("/Users/nicolasblumenroehr/bwSyncShare/VSCode/NEPMappingTool/NEP-Metadata-Mapping-Tool/example/map.json", "/Users/nicolasblumenroehr/bwSyncShare/NEP/DicomTestStudy/Series/small/Archiv.zip")

import time

t1 = time.time()
nums = range(1)
sum = 0
for k in nums:
   Dicom_Mapping("/Users/nicolasblumenroehr/bwSyncShare/VSCode/NEPMappingTool/NEP-Metadata-Mapping-Tool/example/map.json", "/Users/nicolasblumenroehr/bwSyncShare/NEP/DicomTestStudy/Series/small/Archiv.zip")
t2 = time.time()
t = t2 - t1
print("Elapsed time is : ", t, " seconds")