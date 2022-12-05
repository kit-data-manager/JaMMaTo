import pytest
from NEPMetadataMapping.dicomReader import DicomReader

test_dicom_File=DicomReader("fakepath")

def test_dicom_reader(test_dicom_reader: object) -> dict:
    test=DicomReader("fakepath")
    assert list(test.__dict__.keys())==(["studyDateTime", "standardizedName"])


def test_dicom_reader_raises(file=None) -> dict:
    with pytest.raises(TypeError):
        _=DicomReader(file)

def test_dicom_reader_raises(file="fake_path") -> dict:
    with pytest.raises(FileNotFoundError):
        _=DicomReader(file)

@pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ("standardizedname", test_dicom_File.name_standardization("Standardized_name")),
        ("standardizedName", test_dicom_File.name_standardization("Standardized Name")),
    )
)
def test_name_standardization(exp_res: dict, inp: dict) -> None:
    assert exp_res == inp

@pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ({"key1": ["val2", "val1"]}, test_dicom_File.merge_dict_keys({"key1": "val1"}, {"key1": "val2"})),
        ({"key1": ["val2", "val3", "val1"]}, test_dicom_File.merge_dict_keys({"key1": "val1"}, {"key1": ["val2", "val3"]})),
    )
)
def test_merge_dict_keys(exp_res: dict, inp: dict) -> None:
    assert exp_res == inp

'''@pytest.mark.parametrize(
    ("file"),
    (
        (None),
    )
)
def test_dicom_reader_raises(file: str) -> dict:
    with pytest.raises(KeyError):
        _=test_dicom_File.merge_dict_keys({"key1": "val2"}, {})'''