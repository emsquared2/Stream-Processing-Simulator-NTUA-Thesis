import sys


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
            "number_of_keys": (int),
            "arrival_rate": (int),
            "spike_probability": (int),
            "spike_magnitude": (int),
            "distribution":
            {
                "type": "normal | uniform | poisson | zipf",
                "mean": (float)    # Required if type is 'normal'
                "stddev": (float)  # Required if type is 'normal'
                "lambda": (float)  # Required if type is 'poisson'
                "alpha": (float)   # Required if type is 'zipf'
            }
        }

    Raises:
        SystemExit: If any required configuration key is missing or has an invalid value.

    """

    # Define required top-level keys
    required_keys = [
        "streams",
        "steps",
        "number_of_keys",
        "arrival_rate",
        "spike_probability",
        "spike_magnitude",
        "distribution",
    ]
    distribution_required_keys = {
        "normal": ["mean", "stddev"],
        "uniform": [],
        "poisson": ["lambda"],
        "zipf": ["alpha"],
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
    if not isinstance(config["number_of_keys"], int) or config["number_of_keys"] <= 0:
        sys.exit("Invalid value for 'number_of_keys'. Must be a positive integer.")
    if not isinstance(config["arrival_rate"], int) or config["arrival_rate"] <= 0:
        sys.exit("Invalid value for 'arrival_rate'. Must be a positive integer.")
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
            f"Invalid distribution type: {dist_type}. Must be 'uniform', 'normal', 'poisson' or 'zipf'."
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
    print("Valid KeyGenerator.")


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
            sys.exit(f"Missing required key id in stage {i}")
        if stage["id"] != i:
            sys.exit(
                f"Stage IDs must be sequential. Found {stage['id']} at position {i}. Expected {i}."
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

            if "type" not in node or node["type"] not in [
                "stateless",
                "stateful",
                "key_partitioner",
            ]:
                sys.exit(
                    f"Invalid or missing type for node {node['id']} in stage {stage['id']}. Must be 'stateless', 'stateful' or 'key_partitioner'."
                )

            if node["type"] != first_node_type:
                sys.exit(f"All nodes in stage {stage['id']} must have the same type.")

            if "throughput" not in node or node["throughput"] <= 0:
                sys.exit(
                    f"Invalid throughput for node {node['id']} in stage {stage['id']}. Must be a positive number."
                )

            if node["type"] == "stateful" and (
                "complexity_type" not in node
                or node["complexity_type"]
                not in [
                    "O(1)",
                    "O(logn)",
                    "O(n)",
                    "O(nlogn)",
                    "O(n^2)",
                ]
            ):
                sys.exit(
                    f"Invalid or missing complexity_type for node {node['id']} in stage {stage['id']}."
                )

            if node["type"] == "key_partitioner" and (
                "strategy" not in node or not isinstance(node["strategy"], dict)
            ):
                sys.exit(
                    f"Missing or invalid strategy for node {node['id']} in stage {stage['id']}. Must be a dictionary."
                )

            if node["type"] == "key_partitioner":
                strategy = node["strategy"]
                if "name" not in strategy or strategy["name"] not in [
                    "shuffle_grouping",
                    "hashing",
                    "key_grouping",
                    "potc",
                    "pkg",
                ]:
                    sys.exit(
                        f"Invalid or missing strategy name for node {node['id']} in stage {stage['id']}."
                    )

                if strategy["name"] == "key_grouping":
                    if (
                        "prefix_length" not in strategy
                        or strategy["prefix_length"] <= 0
                    ):
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

    print("Valid topology.")
