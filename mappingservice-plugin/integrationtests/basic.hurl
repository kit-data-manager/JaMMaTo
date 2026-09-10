# ----------------------------------------------------------
# Check if the mapping service is reachable
#-----------------------------------------------------------
GET {{host}}
HTTP 200

# ----------------------------------------------------------
# Get mapping types from the mapping service 
# to fetch the first available id
# ----------------------------------------------------------
GET {{host}}/api/v1/mappingAdministration/plugins
HTTP 200
[Captures]
mappingType: regex "(?s)\"id\"\\s*:\\s*\"([^\"]+)\"\\s*,\\s*[^}]*?\"name\"\\s*:\\s*\"Dicom2JSON\""

# ---------------- BEGIN Test Mapping for JaMMaTo -----------

# ----------------------------------------------------------
# Register a dummy mapping with embedded JSON
# ----------------------------------------------------------
POST {{host}}/api/v1/mappingAdministration/
Content-Type: multipart/form-data; boundary=boundary
[Options]
variable: id1=0
```
--boundary
Content-Disposition: form-data; name="record"; filename="blob"
Content-Type: application/json

{"mappingId":"{{id1}}","mappingType": "{{mappingType}}","title":"JaMMaTo from CI test","description":"","acl":[]}
--boundary
Content-Disposition: form-data; name="document"; filename="blob"
Content-Type: application/json

{
    "study": {
        "studyInstanceUid" : "study.studyID"
    },
    "series": {
        "seriesInstanceUid" : "study.series.seriesID"
    }
}
--boundary--
```
HTTP 201

# ----------------------------------------------------------
# Execute mapping with test data
# ----------------------------------------------------------
POST {{host}}/api/v1/mappingExecution/{{id1}}
[MultipartFormData]
document: file,./tests/sampleData/MRIm1.dcm;
HTTP 200
[Captures]
result1: body
[Asserts]
body contains "study"  # Expect some result structure containing "study"

# ----------------------------------------------------------
# Get the ETag of the registered mapping
# ----------------------------------------------------------
GET {{host}}/api/v1/mappingAdministration/{{id1}}
HTTP 200
[Captures]
etag: header "ETag"  # Capture Etag used for delete

# -----------------------------------------------------------
# Delete the registered mapping
# -----------------------------------------------------------
DELETE {{host}}/api/v1/mappingAdministration/{{id1}}
If-Match: {{etag}}
HTTP 204  # Expect a successful deletion

# ---------------- END Test Mapping for JaMMaTo ----------------
