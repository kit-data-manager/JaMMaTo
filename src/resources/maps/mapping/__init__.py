from importlib import resources

files = resources.files(__name__)

mriparser_full = files.joinpath("map_full_path.json")
mriparser_mixed = files.joinpath("map_mixed_path.json")
mriparser_relative = files.joinpath("map_relative_path.json")
mriparser_study = files.joinpath("map_study_only.json")

