import pytest
from unittest.mock import Mock
import pydicom
import os
import zipfile
from jammato.dicom_reader import Dicom_Reader

class IterMixin(object):
    def __iter__(self):
        for value in self.__dict__.values():
            yield value

class Monk_Pydicom_Set_value(IterMixin):

    def __init__(self, value):
        self.__dict__.update({"value": value})
        self.__dict__.update({"name":"Some_Name"})
class Monk_Pydicom_Dataset(IterMixin):

    def __init__(self, multiple_values=True):
        if multiple_values == True:
            key1=Monk_Pydicom_Set_value("20221201")
            key2=Monk_Pydicom_Set_value("092603")
            self.__dict__.update({"value": [[key1],[key2]]})
            self.__dict__.update({"name": "Some_Name"})
        else:
            key1=Monk_Pydicom_Set_value("someValue")
            self.__dict__.update({"value": [key1]})
            self.__dict__.update({"name": "Some_Name"})
class Monk_Pydicom_File(IterMixin):

    def __init__(self):
        self.file1=Monk_Pydicom_Dataset()
        self.file2=Monk_Pydicom_Dataset(multiple_values=False)

class Monk_Pydicom_Object(IterMixin):

    def __init__(self):
        self.file=Monk_Pydicom_File()

@pytest.fixture
def test_dicom_reader(monkeypatch: pytest.MonkeyPatch) -> None:

    def mock_dcmread(file):
        pydicom_file=Monk_Pydicom_Object()
        return pydicom_file

    monkeypatch.setattr(pydicom, "dcmread", mock_dcmread)

    return_validate_type=[True, False, True, False, False, False, False, False, True, False, False]
    validate_type_mock=Mock(side_effect=return_validate_type)
    monkeypatch.setattr(Dicom_Reader, "validate_type", validate_type_mock)

    return_name_standardization=["standardizedName","studyDate", "studyTime", "standardizedName", "standardizedName"]
    name_standardization_mock=Mock(side_effect=return_name_standardization)
    monkeypatch.setattr(Dicom_Reader, "name_standardization", name_standardization_mock)

    return_merge_dict_keys=[{"pixelData": "val1"}, {"pixelData": ["val1", "val2"]}]
    merge_dict_keys_mock=Mock(side_effect=return_merge_dict_keys)
    monkeypatch.setattr(Dicom_Reader, "merge_dict_keys", merge_dict_keys_mock)

@pytest.fixture
def test_metadata_reader_isdir(monkeypatch: pytest.MonkeyPatch) -> None:
    return_is_file=[False, True]
    is_file_mock=Mock(side_effect=return_is_file)
    monkeypatch.setattr(os.path, "isfile", is_file_mock)

    return_is_dir=[True, False]
    is_dir_mock=Mock(side_effect=return_is_dir)
    monkeypatch.setattr(os.path, "isdir", is_dir_mock)

    return_listdir=[["dicom_file"]]
    listdir_mock=Mock(side_effect=return_listdir)
    monkeypatch.setattr(os, "listdir", listdir_mock)

    return_splittext=[("filename", ".dcm")]
    splittext_mock=Mock(side_effect=return_splittext)
    monkeypatch.setattr(os.path, "splitext", splittext_mock)

    return_Dicom_Reader=[None]
    Dicom_Reader_mock=Mock(side_effect=return_Dicom_Reader)
    monkeypatch.setattr(Dicom_Reader, "__init__", Dicom_Reader_mock)

class Monk_Zipfile_name(IterMixin):

    def __init__(self):
        self.filename="dummy_name"

class Monk_Zipfile(IterMixin):

    def __init__(self):
        
        self.filelist=[Monk_Zipfile_name()]

    def __enter__(self):
        return Monk_Zipfile()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def open(self):
        pass

@pytest.fixture
def test_metadata_reader_isfile(monkeypatch: pytest.MonkeyPatch) -> None:
    return_is_file=[True]
    is_file_mock=Mock(side_effect=return_is_file)
    monkeypatch.setattr(os.path, "isfile", is_file_mock)

    return_is_dir=[False]
    is_dir_mock=Mock(side_effect=return_is_dir)
    monkeypatch.setattr(os.path, "isdir", is_dir_mock)

    return_listdir=[["dicom_file"]]
    listdir_mock=Mock(side_effect=return_listdir)
    monkeypatch.setattr(os, "listdir", listdir_mock)

    return_splittext=[("filename", ".dcm")]
    splittext_mock=Mock(side_effect=return_splittext)
    monkeypatch.setattr(os.path, "splitext", splittext_mock)

    return_Dicom_Reader=[None]
    Dicom_Reader_mock=Mock(side_effect=return_Dicom_Reader)
    monkeypatch.setattr(Dicom_Reader, "__init__", Dicom_Reader_mock)
    
    def mock_zipfile(file):
        zipfile=Monk_Zipfile()
        return zipfile

    monkeypatch.setattr(zipfile, "ZipFile", mock_zipfile)

    return_open=["dummy_file"]
    open_mock=Mock(side_effect=return_open)
    monkeypatch.setattr(Monk_Zipfile, "open", open_mock)