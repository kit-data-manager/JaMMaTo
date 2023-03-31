import pytest
from jammato.dicom_reader import Dicom_Reader


def test_dicom_reader(test_dicom_reader: object) -> dict:
    test_dicom_file=Dicom_Reader("fakepath")
    assert list(test_dicom_file.__dict__.keys())==(["studyDateTime", "standardizedName"])


def test_dicom_reader_raises(file=None) -> dict:
    with pytest.raises(TypeError):
        _=Dicom_Reader(file)

def test_dicom_reader_raises(file="fake_path") -> dict:
    with pytest.raises(FileNotFoundError):
        _=Dicom_Reader(file)

@pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ("standardizedname", "Standardized_name"),
        ("standardizedName", "Standardized Name"),
    )
)
def test_name_standardization(test_dicom_reader: object, exp_res: dict, inp: str) -> None:
    test_dicom_file=Dicom_Reader("fakepath")
    assert exp_res == test_dicom_file.name_standardization(inp)

@pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ({"key1": ["val2", "val1"]}, ({"key1": "val1"}, {"key1": "val2"})),
        ({"key1": ["val2", "val3", "val1"]}, ({"key1": "val1"}, {"key1": ["val2", "val3"]})),
    )
)
def test_merge_dict_keys(test_dicom_reader: object, exp_res: dict, inp: dict) -> None:
    test_dicom_file=Dicom_Reader("fakepath")
    assert exp_res == test_dicom_file.merge_dict_keys(inp)
