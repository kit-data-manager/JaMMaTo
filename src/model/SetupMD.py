from pydantic import BaseModel

from mappingservice_plugincore.model.SetupMD import SetupMD as GenericSetupMD

class SetupMD(GenericSetupMD):
    """
    contains metadata derived from file(s) describing the experiment setup
    """
    pass