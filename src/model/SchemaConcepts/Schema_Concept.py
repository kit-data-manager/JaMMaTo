from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import ConfigDict, field_serializer

from pydantic_core.core_schema import SerializerFunctionWrapHandler, SerializationInfo

#Custom deserializer for datetime fields
def parse_datetime(value: str):
    try:
        if "/" in value:
            return datetime.strptime(value, "%m/%d/%Y %H:%M:%S")
        if "." in value:
            return datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
        return datetime.strptime(value, '%d %b %Y %H:%M:%S')#specific handling of expected date format that usual validator cannot handle
    except ValueError:
        return value #not a German date - lets hope that the normal validator can handle it
    

class Schema_Concept(ABC):

    __pydantic_config__ = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    #Custom serializer for datetime fields
    #see https://github.com/pydantic/pydantic/discussions/9275
    @field_serializer("*", mode="wrap")
    def serialize_special_types(
            self,
            value: Any,
            nxt: SerializerFunctionWrapHandler,
            _info: SerializationInfo,
    ):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%dT%H:%M:%SZ')
        return nxt(value)

    @abstractmethod
    def as_schema_class(self):
        """
        Convert the class to the corresponding schema class generated from the json schema
        :return: Schema class
        """
        pass

    def to_schema_dict(self, exclude_none=True) -> dict:
        """
        Return the object data as schema conform dict
        :param exclude_none: set to False if None values should be kept in the dict output (default: True)
        :return: dict of object data
        """
        return self.as_schema_class().model_dump(
            exclude_none=exclude_none,
            mode = "json",
            by_alias=True
        )