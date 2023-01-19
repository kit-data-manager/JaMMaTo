from NEPMetadataMapping.dicom_mapping import Dicom_Mapping
import time

t1 = time.time()
nums = range(100)
sum = 0
for k in nums:
   Dicom_Mapping("/Users/nicoblum/bwSyncShare/VSCode/NEP-Metadata-Mapping-Tool/example/map.json", "/Users/nicoblum/bwSyncShare/NEP/DicomTestStudy/Series/small/Archiv.zip")
t2 = time.time()
t = t2 - t1
print("Elapsed time is : ", t, " seconds")