class MappingAbortionError(Exception):
    """
    Exception that indicates that a severe error occurred that causes preliminary abortion of the mapping.
    Once caught, proper cleanup needs to be performed.
    """