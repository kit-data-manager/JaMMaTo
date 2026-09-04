import os
import pytest

from src.IO.MapfileReader import MapFileReader


class TestMapfileReader:

    def set_up_dir_mapfile(self):
        dir_to_testscript = os.path.split(__file__)[0]
        test_path = os.path.join(dir_to_testscript, "../../src/resources/maps/mapping/")
        return test_path

    def test_read_mapfile_valid(self):
        """The current mapping file keeps the metadata wrapper and the effective sections."""
        tp = self.set_up_dir_mapfile()
        mapfile = os.path.join(tp, "map_full_path.json")

        mapping_dict = MapFileReader.read_mapfile(mapfile)

        assert isinstance(mapping_dict, dict)
        assert "uri" in mapping_dict
        assert "study" in mapping_dict
        assert "series" in mapping_dict
        assert "perImage" in mapping_dict

    def test_mapfile_sections_keep_expected_contract(self):
        """The mapping sections remain accessible under their standard keys."""
        tp = self.set_up_dir_mapfile()
        mapfile = os.path.join(tp, "map_full_path.json")

        mapping_dict = MapFileReader.read_mapfile(mapfile)

        assert mapping_dict["study"]["studyInstanceUid"] == "study.studyID"
        assert mapping_dict["study"]["studyDescription"] == "study.studyTitle"
        assert mapping_dict["series"]["seriesInstanceUid"] == "study.series.seriesID"
        assert mapping_dict["series"]["seriesDescription"] == "study.series.seriesTitle"
        assert mapping_dict["perImage"]["imagePositionpatient"] == "study.series.images.perImage.sampleImagePosition"

    def test_read_mapfile_nonexistent(self):
        """Reading a nonexistent mapping file should still fail."""
        tp = self.set_up_dir_mapfile()
        dummy_file = os.path.join(tp, "dummy.json")

        with pytest.raises(Exception):
            MapFileReader.read_mapfile(dummy_file)

    def test_mapfile_keeps_metadata_wrapper(self):
        """The new system keeps a metadata wrapper in the map payload; tests should reflect that."""
        tp = self.set_up_dir_mapfile()
        mapfile = os.path.join(tp, "map_full_path.json")

        mapping_dict = MapFileReader.read_mapfile(mapfile)

        assert "uri" in mapping_dict
        assert set(mapping_dict.keys()) >= {"uri", "study", "series", "perImage"}

    def test_read_mapfile_supports_wrapped_mapping_payload(self, tmp_path):
        """Wrapped payloads are accepted, but the wrapper remains in the parsed dict."""
        wrapped_map = {
            "mapping": {
                "study": {"studyID": "study.studyID"},
                "series": {"seriesID": "study.series.seriesID"},
                "perImage": {"imageNumber": "study.series.images.perImage.imageNumber"},
            },
        }
        path = tmp_path / "wrapped_map.json"
        path.write_text(__import__("json").dumps(wrapped_map))

        mapping_dict = MapFileReader.read_mapfile(str(path))

        assert set(mapping_dict.keys()) == {"mapping"}
        assert mapping_dict["mapping"]["study"]["studyID"] == "study.studyID"
