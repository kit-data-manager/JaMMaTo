# Example
In order to run the provided example, the user has to install the Python module and add it to the virtual environment the supported Python version is running at.

The easiest way to execute the components of the module is by calling the Dicom_Mapping class, which maps the metadata for any dicom study and a schema. The user then only has to provide the DICOM files of a study as path to the zipped file folder, the metadata map, i.e. the attribute associations from the DICOM standard to the target schema, and a list of 
additional attributes that are nested and repetitive within the DICOM structure, e.g. images of a series.
