# run_mapping.py
import sys
from mapping_cli import run_cli

if __name__ == "__main__":
    # Extract arguments from the command line
    sys.argv = ["mapping_cli"] + sys.argv[1:]

    # Call the run_cli function
    run_cli()