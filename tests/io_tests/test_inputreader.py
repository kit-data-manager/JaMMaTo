import os
import pytest

from src.IO.InputReader import InputReader
from src.parser.impl.MRI_Parser import MRI_Parser


class TestInputReader:

    def set_up_sample_data(self):
        dir_to_testscript = os.path.split(__file__)[0]
        return os.path.join(dir_to_testscript, "../SampleData")

    def test_get_applicable_mriparser(self):
        tp = self.set_up_sample_data()

        dicomfile = os.path.join(tp, "./MRIm1.dcm")

        parsers = InputReader.get_applicable_parsers(dicomfile)
        assert len(parsers) >= 1

        dicomfile = os.path.join(tp, "./MRIm1.dcm")

        parsers = InputReader.get_applicable_parsers(dicomfile)
        assert len(parsers) >= 1

    def test_get_applicable_parsers_with_extension(self):
        tp = self.set_up_sample_data()

        dicomfile = os.path.join(tp, "./MRIm1.dcm")

        parsers = InputReader.get_applicable_parsers(dicomfile)
        assert len(parsers) >= 1
        assert "MRI_Parser" in parsers

    def test_get_applicable_parsers_wo_extension(self):
        tp = self.set_up_sample_data()

        # Create a copy of the DICOM file without extension
        dicomfile_with_ext = os.path.join(tp, "./MRIm1.dcm")
        dicomfile_wo_ext = os.path.join(tp, "./MRIm1")
        
        # Copy the file without extension
        import shutil
        shutil.copy2(dicomfile_with_ext, dicomfile_wo_ext)

        parsers = InputReader.get_applicable_parsers(dicomfile_wo_ext)
        assert len(parsers) >= 1
        
        # Clean up
        if os.path.exists(dicomfile_wo_ext):
            os.unlink(dicomfile_wo_ext)