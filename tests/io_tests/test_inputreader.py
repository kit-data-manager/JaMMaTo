import os
import shutil
import zipfile

from src.IO.InputReader import InputReader
from src.parser import ParserConfig


class TestInputReader:

    def set_up_sample_data(self):
        dir_to_testscript = os.path.split(__file__)[0]
        return os.path.join(dir_to_testscript, "../sampleData")

    def test_input_reader_handles_single_dicom(self):
        tp = self.set_up_sample_data()
        mapfile = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../../src/resources/maps/mapping/map_full_path.json",
        ))
        dicomfile = os.path.join(tp, "./MRIm1.dcm")
        ParserConfig.register_parsers()

        reader = InputReader(mapfile, dicomfile)
        result = reader.retrieve_image_info()

        assert result is not None
        assert "study" in result

    def test_input_reader_handles_dicom_without_extension(self):
        tp = self.set_up_sample_data()
        mapfile = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../../src/resources/maps/mapping/map_full_path.json",
        ))
        dicomfile_with_ext = os.path.join(tp, "./MRIm1.dcm")
        dicomfile_wo_ext = os.path.join(tp, "./MRIm1")
        ParserConfig.register_parsers()

        shutil.copy2(dicomfile_with_ext, dicomfile_wo_ext)
        try:
            reader = InputReader(mapfile, dicomfile_wo_ext)
            result = reader.retrieve_image_info()
            assert result is not None
            assert "study" in result
        finally:
            if os.path.exists(dicomfile_wo_ext):
                os.unlink(dicomfile_wo_ext)

    def test_zip_input_reader_can_extract_and_map_dataset(self, tmp_path):
        src_dir = self.set_up_sample_data()
        dicomfile = os.path.join(src_dir, "MRIm1.dcm")
        zip_path = tmp_path / "dataset.zip"

        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.write(dicomfile, arcname="MRIm1.dcm")

        mapfile = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../../src/resources/maps/mapping/map_full_path.json",
        ))

        reader = InputReader(mapfile, str(zip_path))
        result = reader.retrieve_image_info()

        assert result is not None
        assert "study" in result
        reader.clean_up()

    def test_zip_input_reader_accepts_named_example_archive(self):
        src_dir = self.set_up_sample_data()
        zip_path = os.path.join(src_dir, "7319761.zip")

        assert os.path.exists(zip_path), f"Missing archive fixture: {zip_path}"

        mapfile = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../../src/resources/maps/mapping/map_full_path.json",
        ))

        reader = InputReader(mapfile, zip_path)
        result = reader.retrieve_image_info()

        assert result is not None
        assert isinstance(result, dict)
        assert "study" in result
        reader.clean_up()
