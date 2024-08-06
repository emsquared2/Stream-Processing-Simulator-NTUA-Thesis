import json
import sys
from complexities.Complexities import O1Complexity, OLogNComplexity, ONComplexity, ONLogNComplexity, ON2Complexity, Complexity


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


def validate_config(config):
    """
    Validates the configuration for the key generation and distribution.

    Args:
        config (json): Json object that holds the configuration

    Notes:
        Valid json configurations are the following:

        {
            "streams": (int),
            "steps": (int),
            "number of keys": (int),
            "arrival rate": (int),
            "distribution":
            {
                "type": "normal | uniform",
                "mean": (float)    # Required if type is 'normal'
                "stddev": (float)  # Required if type is 'normal'
            }
        }

    Raises:
        SystemExit: If any required configuration key is missing or has an invalid value.

    """

    # Define required top-level keys
    required_keys = [
        "streams",
        "steps",
        "number of keys",
        "arrival rate",
        "distribution",
    ]
    distribution_required_keys = {
        "normal": ["mean", "stddev"],
        "uniform": [],
    }

    # Check for missing top-level keys
    for key in required_keys:
        if key not in config:
            sys.exit(f"Missing required key: {key}")

    # Check types of top-level keys
    if not isinstance(config["streams"], int) or config["streams"] <= 0:
        sys.exit("Invalid value for 'streams'. Must be a positive integer.")
    if not isinstance(config["steps"], int) or config["steps"] <= 0:
        sys.exit("Invalid value for 'steps'. Must be a positive integer.")
    if not isinstance(config["number of keys"], int) or config["number of keys"] <= 0:
        sys.exit("Invalid value for 'number of keys'. Must be a positive integer.")
    if not isinstance(config["arrival rate"], int) or config["arrival rate"] <= 0:
        sys.exit("Invalid value for 'arrival rate'. Must be a positive integer.")

    # Check 'distribution' dictionary
    if not isinstance(config["distribution"], dict):
        sys.exit("Invalid value for 'distribution'. Must be a dictionary.")

    # Check 'type' in 'distribution'
    distribution = config["distribution"]
    if "type" not in distribution:
        sys.exit("Missing required key in 'distribution': type")

    dist_type = distribution["type"]
    if dist_type not in distribution_required_keys:
        sys.exit(
            f"Invalid distribution type: {dist_type}. Must be 'uniform' or 'normal'."
        )

    # Check required keys for specific distribution types
    required_dist_keys = distribution_required_keys[dist_type]
    for key in required_dist_keys:
        if key not in distribution:
            sys.exit(f"Missing required key for '{dist_type}' distribution: {key}")
        if not isinstance(distribution[key], (int, float)):
            sys.exit(
                f"Invalid value for '{key}' in '{dist_type}' distribution. Must be a number."
            )

    # If all checks pass
    print("Config is valid.")


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
