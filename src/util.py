import json
import logging
from pathlib import Path
import re

import h5py
import pydicom

from magika import Magika
import os
import tempfile
import time
from json import JSONDecodeError
from typing import Optional
import configparser
import numpy as np

import requests
import zipfile

from mappingservice_plugincore.exceptions.MappingAbortionError import MappingAbortionError

def robust_textfile_read(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding="latin1") as file:
                return file.read()
        except UnicodeDecodeError:
            logging.error("Unable to determine file encoding. Aborting.")
            #TODO: since it is not clear who calls this function for what, it may make more sense to raise a unified error to handle instead of error for exit
            raise MappingAbortionError("File loading failed due to encoding.")

def load_json(source) -> Optional[dict]:
    """
    Load JSON data from a local file path or a web URL.

    :param source: A string representing either a local file path or a web URL.
    :return: Parsed JSON data.
    """
    if source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    else:
        return json.loads(robust_textfile_read(source))

def is_zipfile(filepath):
    return zipfile.is_zipfile(filepath)

def extract_zip_file(zip_file_path):
    """
    extracts files of zip to a temporary directory
    :param zip_file_path: local file path to zip file
    :return: (path to contained emxml file, path to tmp dir) or (None, None) if no emxml file was found
    """
    temp_dir = tempfile.mkdtemp()

    start_time = time.time()  # Start time
    logging.info(f"Extracting {zip_file_path}...")

    target_dir = None

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        total_items = len(zip_ref.namelist())

        for index, file_name in enumerate(zip_ref.namelist(), start=1):
            file_path = os.path.join(temp_dir, file_name)
            zip_ref.extract(file_name, temp_dir)

    end_time = time.time()  # End time
    total_time = end_time - start_time

    logging.info(f"Total time taken to process: {total_time:.2f} seconds.")
    return temp_dir

def strip_workdir_from_path(workdirpath, fullpath):
    if fullpath.startswith(workdirpath):
        return fullpath.replace(workdirpath, ".", 1)
    logging.debug("Unable to remove working directory from given path. Returning unchanged path")
    return fullpath

def _import_nxs_as_dict(obj, group=''):
    """
    Recursive function to travel all over the Nexus file tree and extract all data and metadata as a dictionary.
    Inputs:
        obj: h5py (object)
    Output:
        inputFile (dictionary)
    """
    inputFile = {}

    if isinstance(obj, h5py.Group):
        for key in obj.keys(): # Iterate through all items in the group
            full_directory = f"{group}.{key.strip()}" if group else key
            inputFile.update(_import_nxs_as_dict(obj[key], full_directory))
    elif isinstance(obj, h5py.Dataset):
        try:
            # Get dataset information
            dataset_info = {
                'name': obj.name,
                'attributes': dict(obj.attrs)  # Attributes of the dataset
            }

            # Extract the contents of the dataset (Handle scalar and array datasets)
            if isinstance(obj[()], np.ndarray):
                dataset_info['value'] = obj[()]
            else:
                dataset_info['value'] = obj[()].decode('utf-8')

            inputFile[group] = dataset_info # Add dataset info to the main dictionary
        except Exception as e:
            logging.warning(f"Error processing dataset {group}: {e}")
    return {key.replace('/', '.'): value for key, value in inputFile.items()}


def _flat_to_nested_dict(flat_dict):
    nested_dict = {}
    
    for flat_key, value in flat_dict.items():
        keys = flat_key.split('.') # Split the key by dots
        current_level = nested_dict

        for key in keys[:-1]:
            if key not in current_level:
                current_level[key] = {}
            current_level = current_level[key]
        
        current_level[keys[-1]] = value # Assign the value to the last key
    
    return nested_dict

def _dicom_to_nested_dict(ds):
    result = {}

    for attribute in ds:
        # Skip PixelData type (large binary) - VR (Value Representation)
        if attribute.VR in ("OB", "OW", "OF", "OD", "UN"):
            continue

        # Use standardized names to match mapping file expectations
        keyword = attribute.keyword
        name = attribute.name
        standardized = name_standardization(name) if name else None
        
        key = standardized or keyword or str(attribute.tag)

        # Nested type - Sequence
        if attribute.VR == "SQ":
            result[key] = [_dicom_to_nested_dict(item) for item in attribute.value]
            continue

        val = attribute.value

        # JSON-friendly conversion
        if isinstance(val, (bytes, bytearray)):
            result[key] = f"<{len(val)} bytes>"
        elif isinstance(val, (list, tuple)):
            result[key] = [str(v) for v in val]
        elif not isinstance(val, (str, int, float, bool)) and val is not None:
            result[key] = str(val)
        else:
            result[key] = val

    return result

def input_to_dict(stringPayload) -> Optional[dict]:
    if type(stringPayload) is not str:
        return None
    #print("--------im trying--------------", stringPayload)
    try:
        # Check if it's a file path vs JSON content
        if os.path.exists(stringPayload):
            # It's a file path, detect file type
            filetype = get_filetype_with_magica(stringPayload)
            logging.debug(f"Detected filetype: {filetype} for file: {stringPayload}")
        elif stringPayload.startswith("{"):
            # It's JSON content
            try: #JSON
                logging.info("Reading json content was successful!")
                return json.loads(stringPayload)
            except JSONDecodeError:
                logging.debug("Reading input as json not successful")
                return None
        else:
            # Not a file and not JSON, can't process
            logging.debug(f"Cannot process input: {stringPayload}")
            return None
            
        if filetype in ["application/octet-stream", "application/x-hdf5"]:
            try: #NXS
                with h5py.File(stringPayload, 'r') as f:
                    logging.info("Reading neXus/hdf5 file was successful!")
                    return _flat_to_nested_dict(_import_nxs_as_dict(f))
            except Exception as e:
                logging.debug(f"Error reading Nexus/hdf5 file: {e}")
        if filetype in ["application/dicom", "application/x-iso9660-image"]:
            try: #DICOM
                ds = pydicom.dcmread(stringPayload)
                logging.info("Reading dicom file was successful!")
                return _dicom_to_nested_dict(ds)
            except Exception as e:
                logging.debug(f"Error reading DICOM file: {e}")
    except Exception as e:
        logging.warning("Best effort input reading failed with unexpected error. Input malformed?")
        logging.error(e)

def normalize_path(pathString):
    if "\\" in pathString: return os.path.join(*pathString.split("\\"))
    return pathString

def get_filetype_with_magica(filepath):
    m = Magika()
    res = m.identify_path(Path(filepath))
    return res.output.mime_type

def name_standardization(attribute: str) -> str: 
        """Takes a string of a dicom attribute as input and standardizes it after defined criteria.

        Args:
            attribute (str): The attribute string that should be standardized.

        Returns:
            str: The attribute string after standardization.
        """
        name = attribute.split()
        if len(name) == 1:
            name = name[0].lower()
        else:
            subname = ""
            for letter in name[1:]:
                subname += letter.capitalize()
            name = name[0].lower() + subname
        name = re.sub('[^A-Za-z0-9]+', '', name)
        return name