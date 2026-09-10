import os

import pytest

from src.parser.impl.MRI_Parser import MRI_Parser


class TestMRIparser:

    def set_up_sample_data(self):
                dir_to_testscript = os.path.split(__file__)[0]
                return os.path.join(dir_to_testscript, "../sampleData")

    def test_mri_parser_basic(self):
        """The parser reads DICOM metadata grouped by series UID in the current architecture."""
        tp = self.set_up_sample_data()

        try:
            test_dicompath = os.path.join(tp, "./MRIm1.dcm")

            parser = MRI_Parser()
            assert parser is not None

            input_md = parser._read_input_file(test_dicompath)
            assert input_md is not None
            assert isinstance(input_md, dict)
            assert len(input_md) >= 1

            series_uid, series_items = next(iter(input_md.items()))
            assert isinstance(series_uid, str)
            assert isinstance(series_items, list)
            assert len(series_items) >= 1
            assert "instanceCreationDate" in series_items[0]
        except FileNotFoundError:
            pytest.skip("Test file not included, skipping test")

    def test_mri_parser_dicom(self):
        """Reading a DICOM file should not raise and should return a series-grouped structure."""
        tp = self.set_up_sample_data()
        test_dicompath = os.path.join(tp, "./MRIm1.dcm")

        if not os.path.exists(test_dicompath):
            pytest.skip("Optional example DICOM file not included, skipping test")

        parser = MRI_Parser()
        input_md = parser._read_input_file(test_dicompath)

        assert input_md is not None
        assert isinstance(input_md, dict)
        assert len(input_md) >= 1

    def test_mri_parser_preprocessing(self):
        """The parser keeps the series-grouped raw metadata structure after reading."""
        tp = self.set_up_sample_data()

        try:
            test_dicompath = os.path.join(tp, "./MRIm1.dcm")

            parser = MRI_Parser()
            input_md = parser._read_input_file(test_dicompath)

            assert input_md is not None
            assert isinstance(input_md, dict)
            first_series = next(iter(input_md.values()))
            assert isinstance(first_series, list)
            assert len(first_series) >= 1
            assert "studyInstanceUid" in first_series[0]
        except FileNotFoundError:
            pytest.skip("Test file not included, skipping test")