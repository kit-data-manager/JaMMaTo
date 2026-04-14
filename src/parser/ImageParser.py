import enum
from abc import ABC, abstractmethod

from src.model.ImageMD import ImageMD

class ImageParser(ABC):

    @staticmethod
    @abstractmethod
    def expected_input_format() -> str:
        """
        Return expected input format of parser. This can be used to determine if a parser is applicable to the given input.
        :return: mimetype string for input format (such as application/octet-stream)
        """
        pass

    @abstractmethod
    def parse(self, file_path, mapping) -> tuple[ImageMD, str]:
        pass

