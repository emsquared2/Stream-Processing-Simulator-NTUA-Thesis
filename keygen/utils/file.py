import json

def load_config(config_file):
    """Loads the configuration for the key generation and distribution.

    Args:
        config_file (str): Path to the JSON file that holds the configuration.

    Returns:
        dict: The loaded configuration as a dictionary.
    """

    with open(config_file, "r") as file:
        config = json.load(file)
    return config


def write_output(stream, output_file):
    """Write the generated stream to an output file specified from "output_file".

    Args:
        stream (list):  List of strings that represent a step in the stream simulation
                        or a line in the output file.
        output_file (str): Path to the output file where the stream will be written
    """
    with open(output_file, "w") as file:
        for line in stream:
            file.write(line + "\n")