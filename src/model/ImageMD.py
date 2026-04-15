import logging
import os

from pydantic import BaseModel

from src.model.SchemaConcepts.MRI_Image import MRI_Image
from mappingservice_plugincore.model.ImageMD import ImageMD as GenericImageMD


class ImageMD(GenericImageMD[MRI_Image]):

    filePath: str
    image_metadata: MRI_Image = None

    def fileName(self):
        return os.path.basename(self.filePath)

    def folderName(self):
        return os.path.basename(os.path.dirname(self.filePath))