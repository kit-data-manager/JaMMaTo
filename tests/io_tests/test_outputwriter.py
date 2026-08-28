import json

from src.IO.OutputWriter import OutputWriter


def test_output_writer_creates_json_file(tmp_path):
    output = tmp_path / "nested" / "metadata.json"
    metadata = {"study": {"studyID": "test-study"}}

    OutputWriter.writeOutput(metadata, str(output))

    assert output.exists()
    assert json.loads(output.read_text(encoding="utf-8")) == metadata
