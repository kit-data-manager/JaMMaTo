import json

import pytest

from mappingservice_plugincore.exceptions.MappingAbortionError import MappingAbortionError
from src.IO.MapfileReader import MapFileReader


def test_read_local_mapfile(tmp_path):
    mapping_file = tmp_path / "map.json"
    expected = {"study": {"studyInstanceUid": "study.studyID"}}
    mapping_file.write_text(json.dumps(expected), encoding="utf-8")

    assert MapFileReader.read_mapfile(str(mapping_file)) == expected


def test_missing_mapfile_raises_mapping_abortion_error(tmp_path):
    with pytest.raises(MappingAbortionError):
        MapFileReader.read_mapfile(str(tmp_path / "missing.json"))
