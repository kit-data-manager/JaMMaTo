import json
import logging
import os


class OutputWriter:
    """
    Output writer for MRI metadata.
    """

    @staticmethod
    def writeOutput(metadata_dict: dict, output_path: str) -> None:
        """
        Write the metadata dictionary to a JSON file.

        Args:
            metadata_dict (dict):
                Final MRI metadata dictionary.

            output_path (str):
                Path to the output JSON file.
        """

        try:
            output_dir = os.path.dirname(output_path)

            if output_dir and not os.path.exists(output_dir):
                os.makedirs(
                    output_dir,
                    exist_ok=True,
                )

            with open(
                output_path,
                "w",
                encoding="utf-8",
            ) as json_file:

                json.dump(
                    metadata_dict,
                    json_file,
                    indent=4,
                    ensure_ascii=False,
                )

            logging.info(
                "Output successfully written to %s",
                output_path,
            )

        except (OSError, TypeError) as error:
            logging.error(
                "Failed to write output to %s: %s",
                output_path,
                error,
            )
            raise