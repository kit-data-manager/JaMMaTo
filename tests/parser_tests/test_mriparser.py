import json
from pathlib import Path

import pytest

from mappingservice_plugincore.exceptions.MappingAbortionError import MappingAbortionError
from src.parser.impl.MRI_Parser import MRI_Parser
from src.resources.maps.mapping import mriparser_full


SAMPLE_DIR = Path(__file__).parents[1] / "sampleData"


@pytest.fixture
def mapping():
    return json.loads(mriparser_full.read_text())


def test_name_standardization_keeps_historical_jammato_style():
    assert MRI_Parser._name_standardization("Study Instance UID") == "studyInstanceUid"
    assert (
        MRI_Parser._name_standardization("Image Orientation (Patient)")
        == "imageOrientationpatient"
    )


def test_single_dicom_is_mapped(mapping):
    parser = MRI_Parser()
    result, raw = parser.parse(SAMPLE_DIR / "DICOM" / "I0.dcm", mapping)

    assert result is not None
    assert len(raw) == 1

    output = result.image_metadata.to_schema_dict()
    assert output["study"]["studyID"] == (
        "1.3.6.1.4.1.5962.99.1.1761388472.1291962045.1616669124536.2592.0"
    )
    assert len(output["study"]["series"]) == 1


def test_directory_groups_files_by_series_instance_uid(mapping, tmp_path):
    # I0 and I1 share one SeriesInstanceUID; I2 belongs to another series.
    for name in ("I0.dcm", "I1.dcm", "I2.dcm"):
        (tmp_path / name).write_bytes((SAMPLE_DIR / "DICOM" / name).read_bytes())

    parser = MRI_Parser()
    result, raw = parser.parse(tmp_path, mapping)

    assert result is not None
    assert sorted(len(group) for group in raw.values()) == [1, 2]

    output = result.image_metadata.to_schema_dict()
    assert len(output["study"]["series"]) == 2

    series_sizes = sorted(
        len(series["images"].get("perImage", []))
        for series in output["study"]["series"]
    )
    assert series_sizes == [1, 2]


def test_multiframe_dicom_is_expanded_to_per_image_entries(mapping):
    parser = MRI_Parser()
    result, _ = parser.parse(SAMPLE_DIR / "7319761" / "series0.dcm", mapping)

    output = result.image_metadata.to_schema_dict()
    per_image = output["study"]["series"][0]["images"]["perImage"]

    assert len(per_image) == 10
    assert per_image[0]["imageNumber"] == 1
    assert per_image[-1]["imageNumber"] == 10
    assert per_image[0]["sampleImagePosition"] != per_image[-1]["sampleImagePosition"]


def test_files_from_different_studies_are_rejected():
    parser = MRI_Parser()

    parser._analyse_study(
        {
            "studyInstanceUid": "study-A",
            "seriesInstanceUid": "series-A",
            "sopInstanceUid": "sop-A",
        }
    )

    with pytest.raises(MappingAbortionError):
        parser._analyse_study(
            {
                "studyInstanceUid": "study-B",
                "seriesInstanceUid": "series-B",
                "sopInstanceUid": "sop-B",
            }
        )


def test_duplicate_sop_instance_uid_is_detected():
    parser = MRI_Parser()
    metadata = {
        "studyInstanceUid": "study-A",
        "seriesInstanceUid": "series-A",
        "sopInstanceUid": "same-sop",
    }

    first_duplicate, _ = parser._analyse_study(metadata)
    second_duplicate, _ = parser._analyse_study(metadata)

    assert first_duplicate is False
    assert second_duplicate is True
