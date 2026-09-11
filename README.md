
![Tests](https://img.shields.io/github/actions/workflow/status/kit-data-manager/JaMMaTo/python-app.yml?label=Tests)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# JaMMaTo

JaMMaTo (JSON Metadata Mapping Tool) is a Python-based metadata mapping tool designed for mapping metadata from a proprietary file format schema to a JSON format schema. The primary supported input format is DICOM, including multiframe DICOM. The codebase is modular so new input parsers and mapping profiles can be added to support additional formats.

## Usage

### 1. Python Command Line Interface

#### Prerequisites

Minimal supported python version: 3.10

#### Cloning the Repository
To get started, clone the repository and navigate to the project directory:
```
git clone https://github.com/kit-data-manager/JaMMaTo.git
cd JaMMaTo
```

#### Setting Up the Environment
You can optionally set up a virtual environment. Depending on your environment, you may have to use the `python3` alias instead of `python` for the following commands.

Install the required dependencies:
```
pip install -r requirements.txt
```

#### Running the Mapper
To run the mapper, use the `mapping_cli` module:
```
python -m mapping_cli
```

**1. Single DICOM file**

The mapper expects a map file, a metadata file, and a JSON output path:
```
python -m mapping_cli -m <path_to_schema.json> -i <path_to_DICOM_file.dcm> -o <json_output_path>
```

For further information about the necessary map file, see [Mapping README](./src/resources/maps/mapping)

**2. Multiframe DICOM**

The mapper expects a map file, a zip file, and a JSON output path:
```
python -m mapping_cli -m <path_to_schema.json> -i <path_to_zipped_DICOM.zip> -o <json_output_path>
```

For further information about the necessary map file, see [Parsing README](./src/resources/maps/parsing)

### 2. Usage as plugin for the [Mapping-Service](https://github.com/kit-data-manager/mapping-service)

The mapper can be used as a plugin for the [kit-data-manager/Mapping-Service](https://github.com/kit-data-manager/mapping-service). The necessary gradle project to build the plugin is included in the [plugin subfolder](./mappingservice-plugin).
For details on how to build the jar file, see the "Build with Gradle" step in the [github actions pipeline](./.github/workflows/plugin-integration.yml) for the plugin integration test.

Plugin and Python code base share the same semantic versioning, so the plugin version always indicates the specific script version used for mapping. This behaviour can be explicitly overriding 
(for example for testing or for working with older versions of the mapping service). To do this, on gradle build time provide the environment variable `VERSION_OVERRIDE_BY_BRANCH`.
The variable needs to contain a branch name of this repo and branch deletion may break a plugin in use. Only use this option very carefully. Do not use this option for production.

## Testing
Run tests using `pytest`:
```
pytest
```

## Supported instruments and formats

The following list provides the range of formats that have been tested via sample data:
### Image Metadata File Format:
- DICOM (.dcm) and multiframe (.zip)

### Instrument:
- Biospec 152/11 by Bruker BioSpin MRI GmbH

## Structure and components

The key components of the pipeline are the following: the schema reader resolves the target JSON schema and creates a schema skeleton describing the nested structure and data types of the output model. The input reader loads the source data, such as DICOM files or ZIP archives, and delegates parsing to the appropriate image parser. The parser extracts metadata and groups it by study and series. The preprocessor normalizes and cleans the extracted metadata, including datetime merging, unit normalization, and list conversion. The attribute mapper reads the JSON mapping file and maps source attributes to target schema attributes, creating a structured target object. The attribute inserter combines this target object with the schema skeleton to place each value in the correct part of the final JSON document. Finally, the output writer serializes the generated metadata to JSON.

![mappingToolWorkflow (1)](https://user-images.githubusercontent.com/86111342/229125035-0f1d7949-7c09-4281-a173-175a84729e7f.jpg)


## Acknowlegdements

This work was carried out with the support of the EU’s H2020 framework program for research and innovation under grant agreement n. 101007417, NFFA-Europe Pilot.

