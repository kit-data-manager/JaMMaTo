class Schemas_Collector():

    def __init__(self) -> None:
        """Instantiates the class and creates an empty dictionary as attribute.
        """
        self.schemas = {}

    def add_schema(self, uri: str, schema: dict) -> None:
        """Takes as input the string of the URI that resolves to a schema and the schema as dictionary. Creates a new entry in the
        object dictionary, e.g. attribute schemas, where URI is the key and the schema dictionary is the value.

        Args:
            uri (str): The string of the schema URI.
            schema (dict): The dictionary of the JSON schema.
        """
        self.schemas[uri] = schema

    def get_uri(self, uri: str) -> bool:
        """Takes the string of the URI to a schema.

        Args:
            uri (str): The string of the schema URI.

        Returns:
            bool: Returns the boolean if the URI exists in the dictionary of the class attribute schemas.
        """
        return uri in self.schemas

    def get_schema(self, uri: str) -> dict:
        """Takes the URI for a schema as string.

        Args:
            uri (str): The string of the schema URI.

        Returns:
            dict: Returns the JSON schema from the class attribute schemas as dictionary.
        """

        return self.schemas[uri]

schemas_collector_instance = Schemas_Collector()
