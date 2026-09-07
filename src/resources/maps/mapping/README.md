# Input - Output Path Mapping

The map file used for metadata mapping defines the relationship between input paths and output paths in the resulting JSON document. All metadata read from the source input is normalized into a dictionary-like structure to enable unified mapping rules.

This project reads metadata from DICOM-based sources, normalizes it, and maps the values to a target JSON schema according to a user-defined mapping file.

## Map File

All maps are expected to be in JSON format and are structured according to the target schema. The left-hand side of the mapping corresponds to a target field, while the right-hand side corresponds to the source path to be read.

```json
{
  "study": {
    "studyId": "source.study.id",
    "studyTitle": "source.study.title"
  },
  "series": {
    "seriesId": "source.series.id",
    "seriesTitle": "source.series.title"
  },
  "perImage": {
    "imageNumber": "source.image.number"
  }
}
```

The value on the right-hand side is read from the source metadata, while the key on the left-hand side defines where this value is inserted in the output.

Sections such as **study**, **series**, and **perImage** are used to organize the target output.

## Basic Mapping

Type conversion is done automatically and schema-compliant if possible. This functionality mainly remains on the core functionality provided by `pydantic`.

The internal prepropressing provides additional conversion such as simple mapping of common unit representations. This handling at the moment is by no means complete and may need future extension.