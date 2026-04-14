# Input - Output Path Mapping

The map file designed for metadata mapping defines the relation between input path and output path in the resulting json.
All read-in information is read in into a json / dict structure for unified mapping definition.

## Map File

All maps are expected to be in a json format with a list of key: value pairs, where key is a string representing a dotted path in the input data, 
and value is a string representing the corresponding dotted path in the output format.

```json
{
  "path.to.input1": "path.to.output1",
  "path.to.input2": "path.to.output2"
}
```

## Basic Mapping

The mapping definition allows for the following relations:

- 1-to-1: path to a single value on the left to single value on the right (see line 1 and 2 in example below)
- n-to-n: path to a list element on the left is put to a corresponding list element on the right (see line 3 in example below)
- n-to-1: path to list elements on the left is put into a single field on the right. This should usually only be used for duplicate entries that need to be extracted into a single structure (see line 4 in example below)
- 1-to-n: path to a single value on the left, following a pattern recognized by the preprocessor, is mapped to a corresponding list element on the right (see line 5 in the example below)

```json
{
  "path.to.input_value": "path.to.output_value",
  "path.to.input_list[3].value": "path.to.output_value",
  "path.to.input_list[*].value": "path.to.output_list[*].value",
  "path.to.input_list[*].value": "path.to.output_value",
  "path.to.input_*.value": "path.to.output_list[*].value",
}
```

Type conversion is done automatically and schema-compliant if possible. This functionality mainly remains on the core functionality provided by `pydantic`. 
The conversion strategy is non-strict, for example mapping values like 'off' or 'no' to boolean true/false values, if expected by the output schema.

The internal prepropressing provides additional conversion such as simple mapping of common unit representations. This handling at the moment is by no means complete and may need future extension.

## Advanced mapping

Besides mapping complete inputs values to an output field, there is in this case the need to make some arithmetic operations on the input values like finding the maximum, mininimum or average value from an input array. To allow this, a substitution function have been created identified by the [extension of jsonpath-ng](https://github.com/h2non/jsonpath-ng?tab=readme-ov-file#extensions) and developed in the preprocessor. To allow a regex-based definition directly attached to the input path. Make sure to include the backticks, otherwise it will not be recognized as a function attachement.

*Example*

Input:
```
{
   "path.to.value": np.array([1.0, np.nan, 2.0])
}
```

Map (regex pattern and capture group):
```
{
   "path.to.value.`arithmetic`[-1]": "path.to.min_value",
   "path.to.value.`arithmetic`[1]": "path.to.max_value",
   "path.to.value.`arithmetic`[0]": "path.to.average_value"
}
```

Output:
```
{
  "path.to.value.`arithmetic`[-1]": 1.0,
  "path.to.value.`arithmetic`[1]": 2.0,
  "path.to.value.`arithmetic`[0]": 1.5
}
```

## Mapping Examples

To explore the approach for various vendors and input formats, check the files in this folder. Currently, only one has been developed (**vendor:** Elettra-Sincrotrone Trieste synchrotron, **input format:** neXus), but more can be added as needed.

### FAQ

**I want to do something more complicated on the data than defined above, how do I do that?**

> The map file approach tries to provide a way to define and document input handling separately and explicitely to help with extension without coding. It is, however, conceptionally limited in its capabilities. 
More complicated parsing likely needs handling in code instead. This is the case for **arithmetic operations**. Feel free to open an issue to discuss further needs.

**What does * mean in the input or output paths?**

> When * is in an input path, it dynamically resolves all matching keys and applies the mapping to each in an output path with a result like [output0, output1, ...]

**What is `arithmetic`?**

> It’s not a general-purpose function or expression evaluator. It’s a reserved keyword (like a pseudo-function) embedded inside input paths in the mapping file to indicate that a certain field should be statistically reduced before being placed into the output.
