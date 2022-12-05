from NEPMetadataMapping.metadataReader import MetadataReader
from NEPMetadataMapping.dicomReader import DicomReader

def test_dicom_reader_isdir(test_metadata_reader_isdir: object) -> object:
    test=MetadataReader("fakepath")
    assert isinstance(test.all_dicom_series[0], DicomReader)

def test_dicom_reader_isfile(test_metadata_reader_isfile: object) -> object:
    test=MetadataReader("fakepath")
    assert isinstance(test.all_dicom_series[0], DicomReader)