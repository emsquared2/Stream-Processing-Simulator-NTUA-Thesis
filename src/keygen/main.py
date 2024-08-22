import sys
from pathlib import Path
from utils.utils import load_config
from KeyGenerator import KeyGenerator

# TODO: Remove this file


def main(config_file, output_file):
    """
    Main function to initialize the KeyGenerator and start the process.
    """
    config = load_config(config_file)
    keygen = KeyGenerator(config["keygen"])
    keygen.generate_input(output_file)


if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent

    config_file = project_root / "config.json"
    output_file = project_root / "input/stream_output0.txt"

    main(config_file, output_file)
