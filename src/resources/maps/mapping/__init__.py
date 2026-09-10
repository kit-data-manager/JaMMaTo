from importlib import resources

files = resources.files(__name__)

mriparser_full = files.joinpath("map_full_path.json")