from pydantic import BaseModel
from typing import Optional, Dict, Any

from src.model.SchemaConcepts.Schema_Concept import Schema_Concept
from src.model.SchemaConcepts.codegen.SchemaClasses_MRI import MagneticResonanceImagingMriSchema


class MRI_Image(Schema_Concept, BaseModel):

    study: Optional[Dict[str, Any]] = None
    series: Optional[Dict[str, Any]] = None
    perImage: Optional[Dict[str, Any]] = None

    def as_schema_class(self):
        # Handle the mapped data structure following tomo_mapper logic
        # Create the correct structure for MagneticResonanceImagingMriSchema
        study_data = {}
        
        # Add study data directly to study_data
        if self.study and isinstance(self.study, dict):
            study_data.update(self.study)
        
        # Add series data as a list to study_data
        if self.series:
            if 'series' not in study_data:
                study_data['series'] = []
            # Ensure series is always a list
            if isinstance(self.series, list):
                study_data['series'].extend(self.series)
            else:
                study_data['series'].append(self.series)
        
        # Handle perImage data - merge it into the series structure
        if self.perImage:
            if 'series' not in study_data:
                study_data['series'] = [{}]
            
            # Ensure perImage is a list and add it to the first series
            perImage_list = self.perImage if isinstance(self.perImage, list) else [self.perImage]
            
            for series in study_data['series']:
                if 'images' not in series:
                    series['images'] = {}
                if 'perImage' not in series['images']:
                    series['images']['perImage'] = []
                series['images']['perImage'].extend(perImage_list)
        
        # Create the schema with the study data
        return MagneticResonanceImagingMriSchema(study=study_data)