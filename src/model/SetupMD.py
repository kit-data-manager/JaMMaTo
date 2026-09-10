from pydantic import BaseModel

class SetupMD(BaseModel):
    """
    contains metadata derived from file(s) describing the experiment setup
    """
    acquisition_metadata: object = None
