import json
import logging
import re

import pydicom

import os
from typing import Any, Dict, Optional
import mappingservice_plugincore.file_util as core_file_util

from mappingservice_plugincore.exceptions.MappingAbortionError import MappingAbortionError

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
    filetype = core_file_util.get_filetype_with_magica(stringPayload)
    try:
        
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