import os
import pytest

from src.IO.MapfileReader import MapFileReader


class TestMapfileReader:

    def set_up_sample_data(self):
        dir_to_testscript = os.path.split(__file__)[0]
        test_path = os.path.join(dir_to_testscript, "../../src/resources/maps/mapping/")
        return test_path

    def test_read_mapfile_valid(self):
        """Test reading a valid mapping file."""
        tp = self.set_up_sample_data()
        mapfile = os.path.join(tp, "map_full_path.json")
        
        mapping_dict = MapFileReader.read_mapfile(mapfile)
        
        assert isinstance(mapping_dict, dict)
        assert 'study' in mapping_dict
        assert 'series' in mapping_dict
        assert 'perImage' in mapping_dict

    def test_parse_mapinfo_for_study(self):
        """Test parsing study section from mapping."""
        tp = self.set_up_sample_data()
        mapfile = os.path.join(tp, "map_full_path.json")
        
        mapping_dict = MapFileReader.read_mapfile(mapfile)
        study_mapping = MapFileReader.parse_mapinfo_for_study(mapping_dict)
        
        assert isinstance(study_mapping, dict)
        assert 'study.studyID' in study_mapping
        assert 'study.studyTitle' in study_mapping

    def test_parse_mapinfo_for_series(self):
        """Test parsing series section from mapping."""
        tp = self.set_up_sample_data()
        mapfile = os.path.join(tp, "map_full_path.json")
        
        mapping_dict = MapFileReader.read_mapfile(mapfile)
        series_mapping = MapFileReader.parse_mapinfo_for_series(mapping_dict)
        
        assert isinstance(series_mapping, dict)
        assert 'study.series.seriesID' in series_mapping
        assert 'study.series.seriesTitle' in series_mapping

    def test_parse_mapinfo_for_perImage(self):
        """Test parsing perImage section from mapping."""
        tp = self.set_up_sample_data()
        mapfile = os.path.join(tp, "map_full_path.json")
        
        mapping_dict = MapFileReader.read_mapfile(mapfile)
        perImage_mapping = MapFileReader.parse_mapinfo_for_perImage(mapping_dict)
        
        assert isinstance(perImage_mapping, dict)
        assert 'study.series.images.perImage.sampleImagePosition' in perImage_mapping

    def test_parse_mapinfo_missing_sections(self):
        """Test parsing when sections are missing."""
        # Test with empty mapping
        empty_mapping = {}
        
        study_mapping = MapFileReader.parse_mapinfo_for_study(empty_mapping)
        series_mapping = MapFileReader.parse_mapinfo_for_series(empty_mapping)
        perImage_mapping = MapFileReader.parse_mapinfo_for_perImage(empty_mapping)
        
        assert study_mapping == {}
        assert series_mapping == {}
        assert perImage_mapping == {}

    def test_read_mapfile_nonexistent(self):
        """Test reading nonexistent mapping file."""
        tp = self.set_up_sample_data()
        dummy_file = os.path.join(tp, "dummy.json")
        
        with pytest.raises(Exception):
            MapFileReader.read_mapfile(dummy_file)
