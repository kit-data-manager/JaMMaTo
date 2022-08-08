# NFFA-EUROPE PILOT (NEP) Metadata Mapping Tool

This objectoriented mapping tool is based on Python, and is used for mapping metadata from a file format schema to a JSON format schema. Currently, only DICOM format is supported. Formats like Nexus and TIFF are planned for the future.

The mapping tool can be imported as a Python package at: https://pypi.org/project/NEPMetadataMapping/1.0.0/
Supported by Python3-3.8

## Structure and components

The mapping tool is composed of multiple, independently working components. They comprise the following functionalities:
  - Transfer of target JSON schema structure into a Python-based dictionary.
  - Transfer of file format metadata into Python-based objects, referring to the hierarchy of the target schema.
  - Instantiate Python objects of the received maps, where the target schema attributes are assigned with attributes of the file format schema.
  - Mapping of the object metadata to the dictionary, according to the assignment in the maps.

## 1. class: MetadataSchemaReader

This class takes as argument the target JSON schema the file format metadata should be mapped to, and a folder of JSON drafts. The latter is for validation
of the schema referring to at least one of the json drafts. After schema validation, the schema is entangled and transfered into a Python dictionary based on the structure of the schema. Currently, the functionality includes identification of the schema properties, considering the property types, or their definition references.
What is missing yet, is the consideration of enumerations and size restrictions for arrays. 

## 2. class: MetadataReader

This class takes as argument the metadata file directory, identifies the format of the files and calls one one the following classes (currently only one):
   ### 2.1 class: DicomReader
   This class is used to transfer metadata from a dicom file to Pyhton object of the class. It implements the pyDicom module to transfer the metadata key-value pairs to the object. For a DICOM Study that contains multiple Series, multiple DICOM files will be in the directory. Therefore, a corresponding amount of Python objects will be created for each DICOM file.

## 3. map classes

For each metadata file and target schema mapping, the assignment of attributes needs to be defined. Currently, this is done by instantiating Python classes, with fixed attribute value assignments using the MetadataReader objects of the files. For each JSON object, one class with the attribute value assignments is pre-defined. In case a JSON schema contains a property, which is a nested array of objects, this implies input of multiple files. In this case, another map per file is created, which contains the assignment of the attribute values. After instantiation of the objects, 
those maps are connected to the common map. This is planned to be implemented in a more generic approach, where the user can provide the attribute value assignments externally to create the map objects.

## 4. class: MapSchema

This class takes the Python dictionary of the target schema and the map class of the metadata file, containing the key-value pairs of the metadata. Based on the target schema structure, the assigned values are mapped to the proper schema location, considering the schema hierarchy and data types of the attributes. What is currently missing, is the option to use additionalProperties in the JSON schema, as well as consideration of array length, or array enumaration. The result is a JSON-compatible dictionary that can be exported as a JSON document.

## 5. class: DicomMapping

This class imports all class components described above, in order to execute them in a proper order for mapping metadata from a DICOM study to a provided metadata JSON schema. The user then simply uses this class to provide the directories of the files containing the metadata and the schema.
