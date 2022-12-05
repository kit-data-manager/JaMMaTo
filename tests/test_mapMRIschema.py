import pytest

from NEPMetadataMapping.mapMRISchema import Map_MRI_Schema

class Class_for_testing1():
    def __init__(self) -> None:
        self.key8_1="8"

class Class_for_testing2():
    def __init__(self) -> None:
        self.key1="1"
        self.key2="2"
        self.key3="3.0"
        self.key4="True"
        self.key5="None"
        self.key6_1="6"
        self.key7=["7"]
        self.key8=[Class_for_testing1()]
        self.key9="9"
        self.key10="10"
        self.key11=["11"]

dummy_map=Class_for_testing2()
test_schema1 = Map_MRI_Schema({"key1": "int", "key2": "str", "key3": "float", "key4": "bool", "key5": "None", "key6": {"key6_1": "str"}, "key7": ["str"], "key8": [{"key8_1": "str"}],
 "key9": ("str", "int"), "key10": {"value": "str", "unit": "default_unit"}, "key11": {"value": ["str"], "unit": "default_unit"}, "key12": 12}, 
 ["key1", "key2", "key3", "key4", "key5", "key6", "key7", "key8", "key9", "key10", "key11", "key12"], dummy_map, None)

@ pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ({"key1": 1, "key2": "2", "key3": 3.0, "key4": True, "key5": "null", "key6": {"key6_1": "6"}, "key7": ["7"], "key8": [{"key8_1": "8"}], "key9": "9", "key10": {"value": "10", "unit": "default_unit"}, "key11": {"value": ["11"], "unit": "default_unit"}}, 
        test_schema1.fill_json_object(test_schema1.schema_skeleton, test_schema1.key_list, test_schema1.map, test_schema1.main_key)),
    )
)
def test_json_object_search(exp_res: dict, inp: dict) -> None:
    assert exp_res == inp