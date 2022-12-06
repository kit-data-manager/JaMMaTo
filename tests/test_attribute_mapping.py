import pytest
from NEPMetadataMapping.attribute_mapping import Attribute_Mapping
class Dicom_Object():
    def __init__(self) -> None:
        self.attribute1 = "value1"
        self.attribute2 = "value2"
        self.attribute3 = "value3"

dicom_object=Dicom_Object()
map_dict={"object": {"attribute1": "attribute1_1", "attribute2": "attribute2_1", "attribute3": "attribute3_1", "attribute4": "attribute4_1"}}
study_map = Attribute_Mapping.mapping_from_object(dicom_object.__dict__, map_dict, "object")
kwargs={"additional_attribute": {"attribute4_1": "value4"}}
study_map.update_map(**kwargs)
@pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ({"attribute1_1": "value1", "attribute2_1": "value2", "attribute3_1": "value3", "additional_attribute": {"attribute4_1": "value4"}}, study_map.__dict__),
    )
)
def test_name_standardization(exp_res: dict, inp: dict) -> None:
    assert exp_res == inp