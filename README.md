
# JaMMaTo

The software JaMMaTo (JSON Metadata Mapping Tool) is a metadata mapping tool based on Python, and is used for mapping metadata from a proprietary file format schema to a JSON format schema. Currently, only DICOM format is supported. Formats like Nexus and TIFF are planned for the future. The software components can be implemented as separate modules to design a custom software architecture for different use cases besides the one provided.

```bash
# Download and Install via pypi (https://pypi.org/project/jammato/) as Python package.
pip install jammato
```
The pip package requires to execution in a working directory that has a [configs](/configs) folder containing the configuration files.

## Structure and components

The mapping tool is composed of multiple, independently working modules. Summarized, they comprise the following functionalities:
  - Querying and transfer of target JSON schema structure into a Python-based dictionary representing the schema skeleton.
  - Transfer of proprietary file format metadata into Python-based objects.
  - Mapping of the metadata object attributes to the attributes of the target schema, using a JSON-based metadata map.
  - Insertion of the mapped metadata attributes in the correct position of the target schema, using the schema skeleton.

The most important classes are the following: the schema_reader class, which searches the target schema structure and produces a schema skeleton as dictionary that contains the schema attributes as keys and their data types as values, i.e. dictionaries and lists for JSON objects and arrays, and primitive data types. The dicom_reader class that is used to transfer metadata from a dicom file to a Pyhton object of the class. It implements the pydicom module to transfer the metadata key-value pairs to the object. For a DICOM Study that contains multiple Series, multiple DICOM files will be in the directory. Therefore, a corresponding amount of Python objects will be created for each DICOM file. The attribute_mapper class that uses the JSON map containing the attribute assignments of origin and target schema, to map the values of the metadata file objects from the Metadata_Reader_class to the attributes of the target schema. This results in a new class instance, with attributes of the target schema, containing the values of the origin schema, i.e. files. The attribute_inserter class that uses the schema skeleton from the Schema_Reader class and the class object of the Attribute_Mapping class, to insert the mapped attributes, i.e. the values of the origin schema at the correct position in the target JSON schema.

![mappingToolWorkflow (1)](https://user-images.githubusercontent.com/86111342/229125035-0f1d7949-7c09-4281-a173-175a84729e7f.jpg)


For the use case of DICOM mapping, these classes are sequentially executed in the dicom_mapping class, that can be directly used as a module of the PIP package.

For other use cases, or more specific demands of the provided use case, the config files in the config directory and the data_cleaning class need to be adjusted, but usually require no modifications.


