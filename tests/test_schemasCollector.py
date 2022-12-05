import pytest

from NEPMetadataMapping.schemasCollector import SchemasCollector

test1 = SchemasCollector()


'''@ pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        ({"key": "value"}, test1.add_schema("uri_placeholder", {"key": "value"})),
    )
)'''
@ pytest.mark.skip(reason="not implemented")
def test_set_item(exp_res: dict, inp: SchemasCollector) -> None:
    inp.schemas=inp
    assert exp_res == inp