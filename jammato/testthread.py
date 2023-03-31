import time
import math

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dicom_reader import Dicom_Reader
from data_cleaning import data_cleaning_instance

def multithreading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)
def multiprocessing(func, args, workers):
    t1 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res), time.time()-t1

def cpu_heavy(x):
    t1 = time.time()
    print('I am', x)
    count = 0
    for i in range(10**7):
        count += i
    return time.time()-t1

if __name__ == '__main__':
    n_jobs = 10
    t=[]
    for i in range(n_jobs): 
        times=(cpu_heavy(i))
        t.append(times)
    print(sum(t))


if __name__ != '__main__':
    t=0
    l, ti1=multiprocessing(cpu_heavy, range(10), 8)
    print(ti1)
'''def execute(file):
    dicom_series=Dicom_Reader(file)
    sub_dict=Dicom_Reader.pydicom_object_search(dicom_series.pydicom_file)
    return dicom_series

if __name__ != '__main__':
    all_mapped=[]
    t1 = time.time()
    files=["/Users/nicolasblumenroehr/bwSyncShare/NEP/DicomTestStudy/Series/small/series6.dcm"]*1000
    for i in range(len(files)):
        dicom_series=execute(files[i])
        all_mapped.append(dicom_series)

    t2 = time.time()
    ti_ser = t2 - t1
    print(ti_ser)

if __name__ == '__main__':
    files=["/Users/nicolasblumenroehr/bwSyncShare/NEP/DicomTestStudy/Series/small/series6.dcm"]*1000
    t=[]
    ti=0
    l, ti1=multiprocessing(execute, files, 4)
    ti=ti1
    t=l
    print(ti)'''  