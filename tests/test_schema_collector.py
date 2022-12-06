import pytest
from NEPMetadataMapping.schemas_collector import Schemas_Collector

schemasCollectorInstance=Schemas_Collector()
schemasCollectorInstance.add_schema("uri", {"attribute1": "value1"})

@pytest.mark.parametrize(
    ("exp_res", "inp"),
    (
        (True, schemasCollectorInstance.get_uri("uri")),
        ({"attribute1": "value1"}, schemasCollectorInstance.get_schema("uri")),
    )
)
def test_name_standardization(exp_res: dict, inp: dict) -> None:
    assert exp_res == inp