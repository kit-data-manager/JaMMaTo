import pytest
# from Classes.dicomReader import DicomReader

from jammato.schema_reader import Schema_Reader

test_schema1 = Schema_Reader(
    {"properties": {"key1": {"type": "integer"}}})
test_schema2 = Schema_Reader(
    {"properties": {"key2": {"type": "number"}}})
test_schema3 = Schema_Reader(
    {"properties": {"key3": {"type": "string"}}})
test_schema4 = Schema_Reader(
    {"properties": {"key4": {"type": "boolean"}}})
test_schema5 = Schema_Reader(
    {"properties": {"key5": {"type": "string"}}, "$defs": {"key_d5_1": {"type": "string"}}})
test_schema6 = Schema_Reader(
    {"properties": {"key6": {"type": "string"}}, "definitions": {"key_d6_1": {"type": "string"}}})
test_schema7 = Schema_Reader(
    {"properties": {"key7": {"type": "string"}}, "definitions": {"key_d7_1": {"type": "object", "properties": {"key_d7_11": {"type": "string"}}}}})
test_schema8 = Schema_Reader(
    {"properties": {"key8": {"type": "string"}}, "definitions": {"key_d8_1": {"type": "array", "items": {"type": "string"}}}})
test_schema9 = Schema_Reader(
    {"properties": {"key9": {"type": "integer"}, "key9_1": {"type": "number"}, "key9_2": {"type": "boolean"}, "key9_3": {"$ref": "#/definitions/key_d9_1"}}, "definitions": {"key_d9_1": {"type": "string"}}})
test_schema10 = Schema_Reader(
    {"properties": {"key_10": {"$ref": "#/definitions/key_d10_1"}}, "definitions": {"key_d10_1": {"$ref": "#/definitions/key_d10_2"}, "key_d10_2": {"type": "string"}}})
test_schema11 = Schema_Reader(
    {"properties": {"key_11": {"$ref": "#/definitions/key_d11_1"}}, "definitions": {"key_d11_1": {"type": "array", "items": {"type": "string"}}}})
test_schema12 = Schema_Reader(
    {"properties": {"key_12": {"$ref": "#/definitions/key_d12_1"}}, "definitions": {"key_d12_1": {"type": "object", "properties": {"key_d12_11": {"type": "string"}}}}})
test_schema13 = Schema_Reader(
    {"properties": {"key_13": {"type": "array", "items": {"$ref": "#/definitions/key_d13_1"}}}, "definitions": {"key_d13_1": {"type": "string"}}})
test_schema14 = Schema_Reader(
    {"properties": {"key_14": {"type": "array", "items": {"oneOf": [{"type": "string"}, {"type": "integer"}]}}}})
test_schema15 = Schema_Reader(
    {"properties": {"key_15": {"type": "array", "items": {"oneOf": [{"properties": {"key_15_1": {"type": "string"}}}]}}}})
test_schema16 = Schema_Reader(
    {"properties": {"key_16": {"type": "array", "items": {"oneOf": [{"items": {"type": "string"}}]}}}})
test_schema17 = Schema_Reader(
    {"properties": {"key_17": {"type": "object", "properties": {"key_17_1": {"oneOf": [{"type": "string"}, {"type": "integer"}]}}}}})
test_schema18 = Schema_Reader(
    {"properties": {"key_18": {"type": "object", "properties": {"value": {"type": "string"}, "unit": {"type": "string", "default": "someUnit"}}}}})
test_schema19 = Schema_Reader(
    {"properties": {"key_19": {"$ref": "#/definitions/key_d19_1"}}, "definitions": {"key_d19_1": {"oneOf": [{"type": "string"}, {"type": "integer"}]}}})
test_schema20 = Schema_Reader(
    {"properties": {"key_20": {"type": "array", "items": { "type": "array", "items": {"type": "string"}}}}})
test_schema21 = Schema_Reader(
    {"properties": {"key_21": {"type": "array", "items": { "type": "object", "properties": {"key_21_1": {"type": "string"}}}}}})
test_schema22 = Schema_Reader(
    {"properties": {"key_22": {"type": "object", "properties": {"value": {"type": "string"}, "unit": {"type": "string"}}}}})
test_schema23 = Schema_Reader(
    {"properties": {"key23": {"type": "null"}}})
test_schema1_1 = Schema_Reader(
    {"properties": {"key11": {"type": "int"}}})
test_schema2_1 = Schema_Reader(
    {"properties": {"key21": {"type": "float"}}})
test_schema3_1 = Schema_Reader(
    {"properties": {"key31": {"type": "str"}}})
test_schema4_1 = Schema_Reader(
    {"properties": {"key41": {"type": "bool"}}})
test_schema5_1 = Schema_Reader(
    {"properties": {"key51": {"type": ["int", "float", "str", "bool"]}}})
test_schema6_1 = Schema_Reader(
    {"properties": {"key_61": {"$ref": "#/definitions/key_d61_1"}}, "definitions": {"key_d61_1": {"$ref": "/definitions/key_d61_2"}, "key_d61_2": {"type": "string"}}})
test_schema7_1 = Schema_Reader(
    {"properties": {"key_71": {"type": "array", "items": {"$ref": "/definitions/key_d7_1"}}}, "definitions": {"key_d7_1": {"type": "string"}}})
test_schema8_1 = Schema_Reader(
    {"properties": {"key_81": {"type": "array", "items": {"oneOf": [{"key_81_1": {"type": "string"}}]}}}})
test_schema9_1 = Schema_Reader(
    {"properties": {"key_91": {"$ref": "/definitions/key_d91_1"}}})

@ pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ({"key1": "int"}, test_schema1.json_object_search(test_schema1.schema)),
        ({"key2": "float"}, test_schema2.json_object_search(test_schema2.schema)),
        ({"key3": "str"}, test_schema3.json_object_search(test_schema3.schema)),
        ({"key4": "bool"}, test_schema4.json_object_search(test_schema4.schema)),
        ({"key9": "int", "key9_1": "float", "key9_2": "bool", "key9_3": "str"}, test_schema9.json_object_search(test_schema9.schema)),
        ({"key_10": "str"}, test_schema10.json_object_search(test_schema10.schema)),
        ({"key_11": ["str"]}, test_schema11.json_object_search(test_schema11.schema)),
        ({"key_12": {"key_d12_11": "str"}}, test_schema12.json_object_search(test_schema12.schema)),
        ({"key_13": ["str"]}, test_schema13.json_object_search(test_schema13.schema)),
        ({"key_14": ["str", "int"]}, test_schema14.json_object_search(test_schema14.schema)),
        ({"key_15": [{"key_15_1": "str"}]}, test_schema15.json_object_search(test_schema15.schema)),
        ({"key_16": [["str"]]}, test_schema16.json_object_search(test_schema16.schema)),
        ({"key_17": {"key_17_1": ["str", "int"]}}, test_schema17.json_object_search(test_schema17.schema)),
        ({"key_18": {"value": "str", "unit": "someUnit"}}, test_schema18.json_object_search(test_schema18.schema)),
        ({"key_19": ["str", "int"]}, test_schema19.json_object_search(test_schema19.schema)),
        ({"key_20": [["str"]]}, test_schema20.json_object_search(test_schema20.schema)),
        ({"key_21": [{"key_21_1": "str"}]}, test_schema21.json_object_search(test_schema21.schema)),
        ({"key_22": {"value": "str", "unit": "str"}}, test_schema22.json_object_search(test_schema22.schema)),
        ({"key23": None}, test_schema23.json_object_search(test_schema23.schema))
    )
)
def test_json_object_search(exp_res: dict, inp: dict) -> None:
    assert inp == exp_res

@ pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ({"key_d5_1": {"type": "string"}}, test_schema5.definitions),
        ({"key_d6_1": {"type": "string"}}, test_schema6.definitions),
        ({"key_d7_1": {"properties": {"key_d7_11": {"type": "string"}}, "type": "object"}}, test_schema7.definitions),
        ({"key_d8_1": {"items": {"type": "string"}, "type": "array"}}, test_schema8.definitions),
        
    )
)
def test_definitions(exp_res: dict, inp: dict) -> None:
    assert inp == exp_res


@ pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ({"key11": None}, test_schema1_1.json_object_search(test_schema1_1.schema)),
        ({"key21": None}, test_schema2_1.json_object_search(test_schema2_1.schema)),
        ({"key31": None}, test_schema3_1.json_object_search(test_schema3_1.schema)),
        ({"key41": None}, test_schema4_1.json_object_search(test_schema4_1.schema)),
        ({"key51": (None, None, None, None)}, test_schema5_1.json_object_search(test_schema5_1.schema)),
        ({"key_61": None}, test_schema6_1.json_object_search(test_schema6_1.schema)),
        ({"key_71": None}, test_schema7_1.json_object_search(test_schema7_1.schema)),
        ({"key_81": [None]}, test_schema8_1.json_object_search(test_schema8_1.schema)),
        ({}, test_schema9_1.json_object_search(test_schema9_1.schema))
    )
)
def test_schema_false_return(exp_res: dict, inp: Schema_Reader) -> None:
    assert inp == exp_res

@ pytest.mark.skip(reason="not implemented")
def testOther() -> None:
    pass
