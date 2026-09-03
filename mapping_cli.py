import argparse
import logging
import os

from mappingservice_plugincore.exceptions.MappingAbortionError import MappingAbortionError

from src.IO.InputReader import InputReader
from src.IO.OutputWriter import OutputWriter
from src.parser import ParserConfig


logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO").upper()
)


def get_args():
    parser = argparse.ArgumentParser(
        description="JaMMaTo MRI/DICOM mapper"
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input DICOM file or MRI ZIP dataset",
    )
    parser.add_argument(
        "-m",
        "--map",
        required=True,
        help="Mapping file path or remote URI",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output JSON file path",
    )
    return parser.parse_args()


def run_cli():
    args = get_args()
    return run_mri_mapper(args)


def run_mri_mapper(args):
    """Run one MRI mapping. ZIP inputs remain one logical MRI dataset."""
    ParserConfig.register_parsers()

    reader = None
    try:
        reader = InputReader(args.map, args.input)
        output = reader.retrieve_image_info()

        if not output:
            raise MappingAbortionError(
                "Could not retrieve MRI metadata from input."
            )

        OutputWriter.writeOutput(output, args.output)
        logging.info("MRI mapping completed.")
        return output

    except MappingAbortionError as error:
        logging.error("MRI mapping aborted: %s", error)
        raise

    finally:
        if reader is not None:
            reader.clean_up()


if __name__ == "__main__":
    run_cli()
