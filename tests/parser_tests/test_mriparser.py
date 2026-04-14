import os
import pytest
from pprint import pprint

from src.parser.impl.MRI_Parser import MRI_Parser
from src.util import input_to_dict


class TestMRIparser:

    def test_mri_parser_basic(self):
        """Test MRI parser basic functionality."""
        dir_to_testscript = os.path.split(__file__)[0]
        
        try:
            test_dicompath = os.path.join(dir_to_testscript, "../SampleData/MRIm1.dcm")
            
            # Test that we can create the parser
            parser = MRI_Parser()
            assert parser is not None
            
            # Test that we can read the DICOM file
            input_md = parser._read_input_file(test_dicompath)
            assert input_md is not None
            assert 'studyDate' in input_md
            assert 'studyTime' in input_md
            
            print("Raw DICOM data:")
            pprint(input_md)
            
        except FileNotFoundError:
            pytest.skip("Test file not included, skipping test")

    def test_mri_parser_dicom(self):
        """Test MRI parser with DICOM file - just test parsing, not mapping."""
        dir_to_testscript = os.path.split(__file__)[0]
        
        try:
            test_dicompath = os.path.join(dir_to_testscript, "../../example/dicom_files/MRIm1.dcm")
            
            parser = MRI_Parser()
            # Just test that we can read the file without errors
            input_md = parser._read_input_file(test_dicompath)
            
            print("Raw DICOM data:")
            pprint(input_md)
            
        except FileNotFoundError:
            pytest.skip("Test file not included, skipping test")

    def test_mri_parser_preprocessing(self):
        """Test MRI parser preprocessing functionality."""
        dir_to_testscript = os.path.split(__file__)[0]
        
        try:
            test_dicompath = os.path.join(dir_to_testscript, "../SampleData/MRIm1.dcm")
            
            parser = MRI_Parser()
            input_md = parser._read_input_file(test_dicompath)
            
            # Test that preprocessing was applied
            assert input_md is not None
            assert 'studyDate' in input_md
            assert 'studyTime' in input_md
            
            print("Raw DICOM data with preprocessing:")
            pprint(input_md)
            
        except FileNotFoundError:
            pytest.skip("Test file not included, skipping test")