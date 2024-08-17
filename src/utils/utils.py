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


def update_config(config, updates):
    """
    Update the configuration dictionary with the given updates.

    Args:
        config (dict): The original configuration dictionary.
        updates (dict): A dictionary of parameters to update.

    Returns:
        dict: The updated configuration dictionary.
    """
    for key, value in updates.items():
        if key == "topology":
            # Update specific topology stage or nodes
            for stage_update in value.get("stages", []):
                stage_id = stage_update.get("id")
                for stage in config["topology"]["stages"]:
                    if stage["id"] == stage_id:
                        stage.update(stage_update)

        elif key == "simulator":
            # Update simulator settings
            config["simulator"].update(value)

        elif key == "keygen":
            # Update key generation settings
            config["keygen"].update(value)

        elif key == "throughput":
            # Update throughput for all nodes in the topology
            for stage in config.get("topology", {}).get("stages", []):
                for node in stage.get("nodes", []):
                    node["throughput"] = value

        else:
            print(f"Warning: Unrecognized configuration parameter '{key}'")

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


def validate_keygen_config(config):
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
            "spike_probability": (int),
            "spike_magnitude": (int),
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
        "spike_probability",
        "spike_magnitude",
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
    if not isinstance(config["spike_probability"], int) or not (
        0 <= config["spike_probability"] <= 100
    ):
        sys.exit(
            "Invalid value for 'spike_probability'. Must be an integer between 0 and 100."
        )
    if not isinstance(config["spike_magnitude"], (int, float)) or not (
        0 <= config["spike_magnitude"]
    ):
        sys.exit(
            "Invalid value for 'spike_magnitude'. Must be a number greater than 0."
        )

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


def validate_topology(config):
    """
    Validates the topology configuration.

    Args:
        config (dict): The topology configuration dictionary.

    Raises:
        SystemExit: If any required configuration key is missing or has an invalid value.
    """

    if "stages" not in config:
        sys.exit("Missing required key: stages")

    stages = config["stages"]

    if not isinstance(stages, list) or len(stages) == 0:
        sys.exit("Invalid value for 'stages'. Must be a non-empty list.")

    node_ids = set()

    for i, stage in enumerate(stages):
        if "id" not in stage:
            sys.exit(f"Missing required key id in stage {i + 1}")
        if stage["id"] != i + 1:
            sys.exit(
                f"Stage IDs must be sequential. Found {stage['id']} at position {i + 1}. Expected {i + 1}."
            )

        if "nodes" not in stage:
            sys.exit(f"Missing required key: nodes in stage {stage['id']}")

        nodes = stage["nodes"]

        if not isinstance(nodes, list) or len(nodes) == 0:
            sys.exit(
                f"Invalid value for 'nodes' in stage {stage['id']}. Must be a non-empty list"
            )

        # Check that all nodes have the same type
        first_node_type = nodes[0]["type"]

        for node in nodes:
            if "id" not in node:
                sys.exit(f"Missing required key: id in a node in stage {stage['id']}")
            if node["id"] in node_ids:
                sys.exit(f"Node ID {node['id']} is not unique in the topology.")
            node_ids.add(node["id"])

            if "type" not in node or node["type"] not in ["stateless", "stateful"]:
                sys.exit(
                    f"Invalid or missing type for node {node['id']} in stage {stage['id']}. Must be 'stateless' or 'stateful'."
                )

            if node["type"] != first_node_type:
                sys.exit(f"All nodes in stage {stage['id']} must have the same type.")

            if "throughput" not in node or node["throughput"] <= 0:
                sys.exit(
                    f"Invalid throughput for node {node['id']} in stage {stage['id']}. Must be a positive number."
                )

            if "complexity_type" not in node or node["complexity_type"] not in [
                "O(1)",
                "O(logn)",
                "O(n)",
                "O(nlogn)",
                "O(n^2)",
            ]:
                sys.exit(
                    f"Invalid or missing complexity_type for node {node['id']} in stage {stage['id']}."
                )

            if "strategy" not in node or not isinstance(node["strategy"], dict):
                sys.exit(
                    f"Missing or invalid strategy for node {node['id']} in stage {stage['id']}. Must be a dictionary."
                )

            strategy = node["strategy"]
            if "name" not in strategy or strategy["name"] not in [
                "shuffle_grouping",
                "hashing",
                "key_grouping",
            ]:
                sys.exit(
                    f"Invalid or missing strategy name for node {node['id']} in stage {stage['id']}."
                )

            if strategy["name"] == "key_grouping":
                if "prefix_length" not in strategy or strategy["prefix_length"] <= 0:
                    sys.exit(
                        f"Invalid or missing prefix_length for key_grouping strategy in node {node['id']} in stage {stage['id']}."
                    )

            if node["type"] == "stateful":
                if "window_size" not in node or node["window_size"] <= 0:
                    sys.exit(
                        f"Missing or invalid window_size for stateful node {node['id']} in stage {stage['id']}."
                    )
                if "slide" not in node or node["slide"] <= 0:
                    sys.exit(
                        f"Missing or invalid slide for stateful node {node['id']} in stage {stage['id']}."
                    )

            if node["type"] == "stateless" and (
                "window_size" in node or "slide" in node
            ):
                sys.exit(
                    f"Stateless node {node['id']} in stage {stage['id']} should not have window_size or slide."
                )


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
