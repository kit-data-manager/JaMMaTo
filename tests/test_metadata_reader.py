from NEPMetadataMapping.metadata_reader import Metadata_Reader
from NEPMetadataMapping.dicom_reader import Dicom_Reader

def test_dicom_reader_isdir(test_metadata_reader_isdir: object) -> object:
    test=Metadata_Reader("fakepath")
    assert isinstance(test.all_dicom_series[0], Dicom_Reader)

def test_dicom_reader_isfile(test_metadata_reader_isfile: object) -> object:
    test=Metadata_Reader("fakepath")
    assert isinstance(test.all_dicom_series[0], Dicom_Reader)