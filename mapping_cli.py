import argparse
import json
import logging
import os
import sys
import zipfile
import shutil
from pathlib import Path

from src.IO.MappingAbortionError import MappingAbortionError
from src.IO.InputReader import InputReader
from src.IO.OutputWriter import OutputWriter

# Make log level configurable from ENV, defaults to INFO level
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'INFO').upper()
)

def run_cli():
    parser = argparse.ArgumentParser(description='JaMMaTo DICOM Mapper - following tomo_mapper architecture')
    parser.add_argument('-i', '--input', required=True, help='Input DICOM file or zip file')
    parser.add_argument('-m', '--mapping', required=True, help='Mapping file path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')
    
    args = parser.parse_args()
    
    # Use MRI mapper by default (following tomo_mapper logic)
    run_mri_mapper(args)

def run_mri_mapper(args):
    argdict = vars(args)
    INPUT_SOURCE = argdict.get('input')
    MAP_SOURCE = argdict.get('mapping')  # Fixed: use 'mapping' instead of 'map'
    OUTPUT_PATH = argdict.get('output')

    try:
        if zipfile.is_zipfile(INPUT_SOURCE):
            temp_dir = os.path.splitext(INPUT_SOURCE)[0]
            logging.info(f"Extracting ZIP to temporary folder: {temp_dir}")
            extracted_files = []

            with zipfile.ZipFile(INPUT_SOURCE, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Collect all files (filter if needed, e.g., by extension)
            for file_path in Path(temp_dir).rglob("*"):
                if file_path.is_file() and "__MACOSX" not in str(file_path):
                    extracted_files.append(file_path)

            if not extracted_files:
                logging.error("No valid files found in zip archive. Aborting")
                sys.exit(1)

            list_of_file_names = []
            success_count = 0 # number of mapping that has been successful!

            for file in extracted_files:
                file_path = file.with_suffix('')
                logging.info(f"Processing extracted file: {file_path}")
                input_file = str(file)
                try:
                    result = process_input(input_file, MAP_SOURCE)
                    file_name = file_path.name + ".json"
                    OutputWriter.writeOutput(result, file_name)
                    list_of_file_names.append(file_name)
                    success_count += 1
                except MappingAbortionError as e:
                    logging.warning(f"Skipping file {input_file} due to mapping error: {e}")
                except Exception as e:
                    logging.exception(f"Unexpected error processing file {input_file}")

            if success_count > 0:
                logging.info(f"In total {success_count} file(s) were successfully processed.")
                # Combine all results into one file
                combined_results = {}
                for file_name in list_of_file_names:
                    with open(file_name, 'r') as f:
                        file_result = json.load(f)
                        combined_results.update(file_result)
                    os.remove(file_name)  # Clean up individual files
                
                OutputWriter.writeOutput(combined_results, OUTPUT_PATH)
                try:
                    shutil.rmtree(temp_dir)
                    logging.info(f"The temporary folder '{temp_dir}' has been deleted.")
                except Exception as e:
                    logging.error(f"Failed to delete temporary folder: {e}")
            else:
                logging.error("No files could be processed successfully. Aborting.")
                sys.exit(1)

        else:
            result = process_input(INPUT_SOURCE, MAP_SOURCE)
            OutputWriter.writeOutput(result, OUTPUT_PATH)

    except MappingAbortionError as e:
        logging.error(f"Mapping abortion error for {INPUT_SOURCE}: {e}")
        sys.exit(1)

def process_input(input_file, map_source):
    reader = InputReader(map_source, input_file)
    img_info = reader.retrieve_image_info()
    logging.debug(f"IMAGE_INFO: {img_info}")

    if not img_info:
        raise MappingAbortionError(f"Could not retrieve image information for {input_file}.")

    return img_info

if __name__ == '__main__':
    run_cli()
