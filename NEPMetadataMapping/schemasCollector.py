class SchemasCollector():

    def __init__(self) -> None:
        self.schemas = {}

    def add_schema(self, uri, schema) -> None:
        self.schemas[uri] = schema

    def get_uri(self, uri) -> None:
        return uri in self.schemas

    def get_schema(self, uri) -> None:
        return self.schemas[uri]


schemasCollectorInstance = SchemasCollector()
