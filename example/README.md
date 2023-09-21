# Example
In order to run the provided example, the user has to install the Python module and add it to the environment the supported Python version is running at.

## Using the cloned repository:
The easiest way to execute the mapping script is by calling the Dicom_Mapping module which maps the metadata for any dicom study and a schema. The user then only has to provide the DICOM files of a study as path to the zipped file folder, the metadata map, i.e. the attribute associations from the DICOM standard to the target schema, and a list of additional attributes that are nested and repetitive within the DICOM structure, e.g. images of a series.
## Using the PyPi Package:
After installation, import the jammato package and use the Dicom_Mapping module as provided in the [dicom_mapping_script](../dicom_mapping_script.py). In this case, the [configuration](../configs) folder with the configuration files has to be added to the same directory where the script is executed.
