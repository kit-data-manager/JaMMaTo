import json
import logging
import os


class OutputWriter:
    """
    Output writer for MRI data following tomo_mapper architecture
    """

    @staticmethod
    def writeOutput(metadata_dict, output_path):
        """
        Write the metadata dictionary to a JSON file
        :param metadata_dict: the metadata dictionary to write
        :param output_path: path to the output file
        """
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            with open(output_path, 'w', encoding="utf-8") as json_file:
                json.dump(metadata_dict, json_file, indent=4, ensure_ascii=False)
            
            logging.info(f"Output successfully written to {output_path}")
            
        except Exception as e:
            logging.error(f"Failed to write output to {output_path}: {e}")
            raise
