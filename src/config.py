import os.path


class MappingConfig:

    working_dir = None

    @classmethod
    def set_working_dir(cls, working_dir):
        cls.working_dir = os.path.normpath(working_dir)

    @classmethod
    def get_working_dir(cls):
        return cls.working_dir
