from pathlib import Path

from src.IO.InputReader import InputReader
from src.parser import ParserConfig
from src.resources.maps.mapping import mriparser_full


SAMPLE_DIR = Path(__file__).parents[1] / "sampleData"


def test_single_mri_file_is_processed():
    ParserConfig.register_parsers()

    reader = InputReader(
        str(mriparser_full),
        str(SAMPLE_DIR / "MRIm1.dcm"),
    )

    try:
        output = reader.retrieve_image_info()
        assert output is not None
        assert len(output["study"]["series"]) == 1
    finally:
        reader.clean_up()