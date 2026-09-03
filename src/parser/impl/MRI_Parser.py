import json
import logging
import os
import re
from typing import Any

import pydicom

from mappingservice_plugincore.exceptions.MappingAbortionError import (
    MappingAbortionError,
)
from mappingservice_plugincore.parser.ImageParser import ImageParser

from src.Preprocessor import Preprocessor
from src.model.ImageMD import ImageMD
from src.model.SchemaConcepts.MRI_Image import MRI_Image
from src.parser.mapping_util import map_a_dict
from src.resources.maps.mapping import mriparser_full


class MRI_Parser(ImageParser):
    """
    MRI/DICOM parser preserving the core JaMMaTo behaviour while following
    the common mapper architecture.

    Responsibilities:
    - read a single DICOM file or a directory of extracted DICOM files
    - flatten DICOM attributes to JaMMaTo-style camelCase names
    - validate that all files belong to the same StudyInstanceUID
    - detect duplicate SOPInstanceUID values
    - group DICOM files by SeriesInstanceUID
    - preprocess metadata series by series
    - map study, series and per-image metadata to the MRI schema structure
    """

    internal_mapping = None

    def __init__(self):
        self.internal_mapping = json.loads(mriparser_full.read_text())
        self._reset_study_analysis()

    @staticmethod
    def expected_input_format():
        return [
            "application/octet-stream",
            "application/dicom",
        ]

    def parse(self, file_path, mapping):
        """
        Parse either a single DICOM file or an extracted MRI dataset directory.

        Returns:
            tuple[ImageMD | None, dict | None]: mapped image metadata and the
            preprocessed raw metadata grouped by SeriesInstanceUID.
        """
        self._reset_study_analysis()

        series_dict = self._read_input_file(file_path)
        if not series_dict:
            logging.warning("No metadata extractable from %s", file_path)
            return None, None

        mapping_dict = mapping if mapping else self.internal_mapping
        if not mapping_dict:
            raise MappingAbortionError("No mapping provided for MRI parsing.")

        # Historical JaMMaTo Data_Cleaning behaviour, now hosted by Preprocessor.
        series_dict = Preprocessor.preprocess_series(series_dict)

        output_metadata = self._map_study(series_dict, mapping_dict)
        if not output_metadata or "study" not in output_metadata:
            logging.warning("No MRI metadata could be mapped from %s", file_path)
            return None, None

        # Mapper-specific post-mapping normalization.
        Preprocessor.normalize_all_units(output_metadata)
        Preprocessor.normalize_string_lists(output_metadata)
        Preprocessor.normalize_program_field(output_metadata)

        try:
            mri_image = MRI_Image(study=output_metadata["study"])
            # Validate against the generated MRI schema before returning.
            mri_image.as_schema_class()
            image_md = ImageMD(
                filePath=str(file_path),
                image_metadata=mri_image,
            )
        except Exception as error:
            logging.error("Mapped MRI metadata does not conform to the schema: %s", error)
            raise MappingAbortionError("MRI schema validation failed.") from error

        return image_md, series_dict

    def _reset_study_analysis(self):
        """Reset state previously maintained by the historical Analyse_Study."""
        self.study_instance_uid = None
        self.all_sop_instance_uids = []
        self.all_series_instance_uids = []

    def _read_input_file(self, file_path: str) -> dict:
        """
        Read either a single DICOM file or a directory containing DICOM files.

        ZIP extraction is handled by InputReader before this method is called.
        """
        if os.path.isdir(file_path):
            return self._read_dicom_directory(file_path)
        return self._read_single_dicom(file_path)

    def _read_single_dicom(self, file_path: str) -> dict:
        """Read one DICOM file and return a one-series dictionary."""
        try:
            dataset = pydicom.dcmread(file_path, stop_before_pixels=True)
        except (pydicom.errors.InvalidDicomError, FileNotFoundError, OSError) as error:
            logging.warning("Unable to read DICOM file %s: %s", file_path, error)
            return {}

        metadata = self._pydicom_object_search(dataset)
        duplicate_sop, _ = self._analyse_study(metadata)

        if duplicate_sop:
            logging.warning("Duplicate SOPInstanceUID found in %s.", file_path)
            return {}

        series_uid = metadata.get("seriesInstanceUid")
        if not series_uid:
            logging.warning("No SeriesInstanceUID found in %s.", file_path)
            return {}

        return {series_uid: [metadata]}

    def _read_dicom_directory(self, directory_path: str) -> dict:
        """
        Read all valid DICOM files recursively and group them by
        SeriesInstanceUID.
        """
        all_dicom_series_dict = {}

        for root, directories, filenames in os.walk(directory_path):
            # Ignore common archive artefacts deterministically.
            directories[:] = sorted(d for d in directories if d != "__MACOSX")

            for filename in sorted(filenames):
                if filename.startswith("._") or filename == ".DS_Store":
                    continue

                file_path = os.path.join(root, filename)

                try:
                    dataset = pydicom.dcmread(file_path, stop_before_pixels=True)
                except (
                    pydicom.errors.InvalidDicomError,
                    FileNotFoundError,
                    IsADirectoryError,
                    PermissionError,
                    OSError,
                ):
                    continue

                metadata = self._pydicom_object_search(dataset)
                duplicate_sop, duplicate_series = self._analyse_study(metadata)

                if duplicate_sop:
                    logging.warning(
                        "Duplicate SOPInstanceUID found. Skipping %s.", file_path
                    )
                    continue

                series_uid = metadata.get("seriesInstanceUid")
                if not series_uid:
                    logging.warning(
                        "No SeriesInstanceUID found. Skipping %s.", file_path
                    )
                    continue

                if duplicate_series:
                    all_dicom_series_dict[series_uid].append(metadata)
                else:
                    all_dicom_series_dict[series_uid] = [metadata]

        return all_dicom_series_dict

    @classmethod
    def _pydicom_object_search(cls, dataset) -> dict:
        """
        Historical Dicom_Reader.pydicom_object_search logic.

        DICOM names are flattened into JaMMaTo-style camelCase keys. DICOM
        sequences are traversed recursively and repeated sequence values are
        merged into lists.
        """
        metadata = {}

        for attribute in dataset:
            if isinstance(attribute.value, pydicom.sequence.Sequence):
                if len(attribute.value) > 1:
                    merged_sequence = {}
                    for sequence_dataset in attribute.value:
                        nested = cls._pydicom_object_search(sequence_dataset)
                        merged_sequence = cls._merge_dict_keys(
                            nested,
                            merged_sequence,
                        )
                    metadata.update(merged_sequence)
                elif len(attribute.value) == 1:
                    metadata.update(
                        cls._pydicom_object_search(attribute.value[0])
                    )
                continue

            name = cls._name_standardization(attribute.name)
            if not name:
                continue

            value = attribute.value

            if isinstance(value, pydicom.multival.MultiValue):
                metadata[name] = Preprocessor.transfer_to_list(value)
            elif isinstance(value, pydicom.valuerep.PersonName):
                metadata[name] = str(value)
            elif isinstance(value, pydicom.uid.UID):
                metadata[name] = str(value)
            elif isinstance(value, (pydicom.valuerep.DSfloat, pydicom.valuerep.IS)):
                # Keep historical JaMMaTo behaviour. Pydantic later converts
                # numeric schema fields to their declared types.
                metadata[name] = str(value)
            elif isinstance(value, bytes):
                # Binary metadata is not useful for the MRI schema mapping and
                # must not leak into the JSON output.
                continue
            else:
                metadata[name] = value

        return metadata

    @staticmethod
    def _name_standardization(attribute_name: str) -> str:
        """
        Historical Dicom_Reader.name_standardization logic.

        Examples:
            Study Instance UID -> studyInstanceUid
            Image Orientation (Patient) -> imageOrientationpatient
        """
        words = attribute_name.split()
        if not words:
            return ""

        if len(words) == 1:
            name = words[0].lower()
        else:
            name = words[0].lower() + "".join(word.capitalize() for word in words[1:])

        return re.sub(r"[^A-Za-z0-9]+", "", name)

    @classmethod
    def _merge_dict_keys(cls, new_dict: dict, merged_dict: dict) -> dict:
        """Historical Dicom_Reader.merge_dict_keys behaviour for sequences."""
        if not merged_dict:
            return dict(new_dict)

        result = dict(merged_dict)

        for key, value in new_dict.items():
            if key not in result:
                result[key] = value
                continue

            current = result[key]
            if isinstance(current, list):
                if isinstance(value, list) and current and not isinstance(current[0], list):
                    current = [current]
                current.append(value)
                result[key] = current
            else:
                result[key] = [current, value]

        return result

    def _analyse_study(self, metadata: dict) -> tuple[bool, bool]:
        """
        Historical Analyse_Study logic.

        Returns:
            tuple[bool, bool]: duplicate SOP flag and duplicate series flag.
        """
        study_uid = metadata.get("studyInstanceUid")
        sop_uid = metadata.get("sopInstanceUid")
        series_uid = metadata.get("seriesInstanceUid")

        if self.study_instance_uid is None:
            self.study_instance_uid = study_uid
        elif study_uid is not None and self.study_instance_uid != study_uid:
            raise MappingAbortionError("DICOM files are not from the same study.")

        duplicate_sop = False
        if sop_uid is not None:
            duplicate_sop = sop_uid in self.all_sop_instance_uids
            if not duplicate_sop:
                self.all_sop_instance_uids.append(sop_uid)

        duplicate_series = False
        if series_uid is not None:
            duplicate_series = series_uid in self.all_series_instance_uids
            if not duplicate_series:
                self.all_series_instance_uids.append(series_uid)

        return duplicate_sop, duplicate_series

    def _map_study(self, series_dict: dict, mapping_dict: dict) -> dict:
        """
        Construct the nested MRI schema document while preserving JaMMaTo's
        study/series/perImage model.
        """
        all_series = list(series_dict.values())
        if not all_series or not all_series[0]:
            return {}

        first_metadata = all_series[0][0]
        study_mapping = mapping_dict.get("study", {})
        series_mapping = mapping_dict.get("series", {})
        per_image_mapping = mapping_dict.get("perImage", {})

        if not study_mapping or not series_mapping:
            raise MappingAbortionError(
                "MRI mapping must define at least 'study' and 'series' sections."
            )

        mapped_study = map_a_dict(first_metadata, study_mapping)
        output_metadata = (
            mapped_study
            if "study" in mapped_study
            else {"study": mapped_study}
        )
        output_metadata.setdefault("study", {})["series"] = []

        for _, metadata_objects in series_dict.items():
            if not metadata_objects:
                continue

            representative = metadata_objects[0]
            mapped_series = map_a_dict(representative, series_mapping)
            series_content = self._extract_series_content(mapped_series)
            if not isinstance(series_content, dict):
                continue

            per_image_list = []
            if per_image_mapping:
                for metadata in metadata_objects:
                    per_image_inputs = self._expand_per_image_metadata(
                        metadata,
                        per_image_mapping,
                    )

                    for per_image_input in per_image_inputs:
                        try:
                            mapped_image = map_a_dict(
                                per_image_input,
                                per_image_mapping,
                            )
                        except MappingAbortionError:
                            # perImage contains optional DICOM attributes; absence
                            # in one frame/file should not invalidate the study.
                            continue

                        image_content = self._extract_per_image_content(mapped_image)
                        if image_content:
                            per_image_list.append(image_content)

            images = series_content.setdefault("images", {})
            if per_image_list:
                images["perImage"] = per_image_list

            output_metadata["study"]["series"].append(series_content)

        return output_metadata


    @staticmethod
    def _expand_per_image_metadata(metadata: dict, per_image_mapping: dict) -> list[dict]:
        """
        Expand multi-frame DICOM per-image attributes into one mapping input per
        frame. This replaces the historical Dicom_Mapping.series_extension()
        behaviour while keeping the same responsibility.

        A simple list such as ImagePositionPatient=[x, y, z] is one value for
        one image and must stay intact. A list of frame values such as
        InStackPositionNumber=[1, 2, ...] or ImagePositionPatient=[[...], [...]]
        is expanded frame by frame.
        """
        source_keys = list(per_image_mapping.keys())
        frame_count = 1

        for key in source_keys:
            value = metadata.get(key)
            if not isinstance(value, list) or not value:
                continue

            if value and isinstance(value[0], list):
                frame_count = max(frame_count, len(value))
            elif key == "instackPositionNumber":
                frame_count = max(frame_count, len(value))

        if frame_count == 1:
            return [metadata]

        expanded = []
        for index in range(frame_count):
            frame_metadata = dict(metadata)

            for key in source_keys:
                value = metadata.get(key)
                if not isinstance(value, list) or len(value) != frame_count:
                    continue

                if key == "instackPositionNumber" or (
                    value and isinstance(value[0], list)
                ):
                    frame_metadata[key] = value[index]

            expanded.append(frame_metadata)

        return expanded

    @staticmethod
    def _extract_series_content(mapped_series: dict) -> dict:
        """Extract one series object from map_a_dict output."""
        content: Any = mapped_series

        if isinstance(content, dict) and "study" in content:
            content = content["study"]
        if isinstance(content, dict) and "series" in content:
            content = content["series"]
        if isinstance(content, list):
            return content[0] if content else {}
        return content if isinstance(content, dict) else {}

    @staticmethod
    def _extract_per_image_content(mapped_image: dict) -> dict:
        """Extract one perImage object from map_a_dict output."""
        content: Any = mapped_image

        if isinstance(content, dict) and "study" in content:
            content = content["study"]
        if isinstance(content, dict) and "series" in content:
            content = content["series"]
            if isinstance(content, list):
                content = content[0] if content else {}
        if isinstance(content, dict) and "images" in content:
            content = content["images"]
        if isinstance(content, dict) and "perImage" in content:
            content = content["perImage"]
        if isinstance(content, list):
            return content[0] if content else {}
        return content if isinstance(content, dict) else {}
