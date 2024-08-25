import json
import sys
from complexities.Complexities import (
    O1Complexity,
    OLogNComplexity,
    ONComplexity,
    ONLogNComplexity,
    ON2Complexity,
    Complexity,
)


def load_config(config_file):
    """
    Loads the configuration file.

    Args:
        config_file (str): Path to the JSON file that holds the configuration.

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    try:
        with open(config_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, IOError) as e:
        sys.exit(f"Error: {e}")


def update_config(config, **kwargs):
    """
    Update the configuration with the provided keyword arguments.

    Args:
        config (dict): The original configuration dictionary.
        **kwargs: Parameters to be modified in the configuration. Supports updating any attribute.

    Returns:
        dict: The updated configuration dictionary.
    """

    # Update keygen configuration if needed
    keygen_updates = {k: v for k, v in kwargs.items() if k in config["keygen"]}
    config["keygen"].update(keygen_updates)

    # Update topology configurations
    for stage in config["topology"]["stages"]:
        for node in stage["nodes"]:
            # If a specific node ID is provided, update only that node
            if "node_id" in kwargs and node["id"] == kwargs["node_id"]:
                # Update attributes of the node
                for attr, value in kwargs.items():
                    if attr in node:
                        node[attr] = value
            else:
                # If no specific node ID is provided, update all nodes with relevant attributes
                for attr, value in kwargs.items():
                    if attr in node:
                        node[attr] = value

    return config


def write_output(stream, output_file):
    """
    Writes the generated stream to an output file specified from "output_file".

    Args:
        stream (list):  List of strings that represent a step in the stream simulation
                        or a line in the output file.
        output_file (str): Path to the output file where the stream will be written.
    """
    with open(output_file, "w") as file:
        file.writelines(line + "\n" for line in stream)


def load_steps_from_file(file_path):
    """
    Loads simulation key steps from input file.

    Args:
        file_path (string): Path to the stream simulator step input file.

    Returns:
        list: A list of lists, where each inner list contains keys for one simulation step.

    """
    steps_data = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                step = line.strip().split(" ")
                # Add the step to the steps_data list
                steps_data.append(step)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        sys.exit(1)
    except IOError:
        print(f"Error: An IOError occurred while reading the file {file_path}.")
        sys.exit(1)
    return steps_data


def create_complexity(complexity_type: str) -> Complexity:
    if complexity_type == "O(1)":
        return O1Complexity()
    elif complexity_type == "O(logn)":
        return OLogNComplexity()
    elif complexity_type == "O(n)":
        return ONComplexity()
    elif complexity_type == "O(nlogn)":
        return ONLogNComplexity()
    elif complexity_type == "O(n^2)":
        return ON2Complexity()
    else:
        raise ValueError(f"Unknown complexity type: {complexity_type}")
