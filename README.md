
# NFFA-EUROPE PILOT (NEP) Metadata Mapping Tool

This objectoriented mapping tool is based on Python, and is used for mapping metadata from a file format schema to a JSON format schema. Currently, only DICOM format is supported. Formats like Nexus and TIFF are planned for the future.

```bash
# Download and Install via pypi (https://pypi.org/project/NEPMetadataMapping/) as Python package.
pip install NEPMetadataMapping
```

## Structure and components

The mapping tool is composed of multiple, independently working modules. Summarized, they comprise the following functionalities:
  - Querying and transfer of target JSON schema structure into a Python-based dictionary representing the schema skeleton.
  - Transfer of proprietary file format metadata into Python-based objects.
  - Mapping of the metadata object attributes to the attributes of the target schema, using a JSON-based metadata map.
  - Insertion of the mapped metadata attributes in the correct position of the target schema, using the schema skeleton.

## Cache_Schemas class
This class uses the URI from the JSON metadata map to cache schemas. Uses the following class to deposit and query the schemas:
  ### Schemas_Collector class
  This class contains a dictionary of schema resolving URIs as keys and corresponding JSON schemas as dictionaries that can be used to cached already downloaded schemas.

## Dicom_Mapping class
This class imports all modules, relevant for mapping from DICOM files to a JSON schema, in order to execute them in a proper order. The user then simply instantiates this class to provide the directories of the files containing the metadata and the JSON map containing attribute assignments and the target schema. The following classes are all executed via this class.

## Schema_Reader class

This class searches the target schema structure and produces a schema skeleton as dictionary that contains the schema attributes as keys and their data types as values, i.e. dictionaries and lists for JSON objects and arrays, and primitive data types.

## Metadata_Reader class

This class identifies the format of the proprietary files and calls one the following classes (currently only one):

  ### Dicom_Reader class
  This class is used to transfer metadata from a dicom file to a Pyhton object of the class. It implements the pydicom module to transfer the metadata key-value pairs to the object. For a DICOM Study that contains multiple Series, multiple DICOM files will be in the directory. Therefore, a corresponding amount of Python objects will be created for each DICOM file.

## Attribute_Mapping class

This class uses the JSON map containing the attribute assignments of origin and target schema, to map the values of the metadata file objects from the Metadata_Reader_class to the attributes of the target schema. This results in a new class instance, with attributes of the target schema, containing the values of the origin schema, i.e. files.

## Map_Schema class

This class uses the schema skeleton from the Schema_Reader class and the class object of the Attribute_Mapping class, to insert the mapped attributes, i.e. the values of the origin schema at the correct position in the target JSON schema. It contains the following class that inherits from this class and introduces specifications for particular use cases:

  ### Map_MRI_Schemas class

  Introduces additional positioning for the MRI schema that contains properties that are divided into values and units attributes.