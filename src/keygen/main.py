import random
import sys
import os
from pathlib import Path
from collections import Counter
from utils import validate_config, load_config, write_output
from distributions.normal import NormalDistribution
from distributions.uniform import UniformDistribution


def create_key_array(length, key=False):
    """
    Creates an array of keys or integers based on the provided length and key flag.

    Args:
        length (int): The length of the array to be created.
        key (bool): If True, the array will contain keys in the format 'key0', 'key1', etc.
                    If False, the array will contain integers as strings, i.e., '0', '1', etc.

    Returns:
        list: A list containing the generated keys or integers.

    Example:
        >>> create_key_array(3, key=True)
        ['key0', 'key1', 'key2']

        >>> create_key_array(3, key=False)
        ['0', '1', '2']
    """

    return [f"key{i}" if key else f"{i}" for i in range(length)]


def adjust_or_create_key_dist(key_array, swap):
    """
    Creates or adjusts the key distribution based on swap flag.
    Used to change the key hierarchy from step to step.
    On the initialization we choose arbitrarily a key frequency hierarchy (shuffle).
    On the next steps each key can change its hierarchical position by at max of 1 position.

    Args:
        key_array (list): List of keys to be adjusted or shuffled.
        swap (bool): Flag indicating whether to adjust (True) or create | shuffle (False) the key distribution.

    Returns:
        list: The adjusted or newly created key array frequency hierarchy.

    Example:
        >>> adjust_or_create_key_dist(['key0', 'key1', 'key2', 'key3'], True)
        ['key0', 'key2', 'key1', 'key3']  # Example output, actual output may vary

        >>> adjust_or_create_key_dist(['key0', 'key1', 'key2', 'key3'], False)
        ['key2', 'key0', 'key3', 'key1']  # Example output, actual output may vary
    """
    if swap:
        n = len(key_array)
        prev_swap = False

        for i in range(n):
            # Determine if the key can move up, down, or stay in place
            possible_moves = [0]  # stay in place
            if i == n - 1:
                possible_moves.append(-1)  # move up
            if i < n - 1:
                possible_moves.append(1)  # move down

            move = random.choice(possible_moves)
            if move != 0 and not prev_swap:
                # Swap the keys in the array
                key_array[i], key_array[i + move] = (key_array[i + move], key_array[i])
                prev_swap = True
            else:
                prev_swap = False
        return key_array

    else:
        random.shuffle(key_array)
        return key_array


def replace_step_with_keys(step, keys):
    """
    Replaces each element in the input list (step) with a corresponding key based on frequency.

    The function first calculates the frequency of each element in the input list.
    It then sorts the elements by their frequency in descending order.
    Each element is then mapped to a key from the provided `keys` list based on this frequency order.

    Args:
        step (list): List of elements where each element is to be replaced based on its frequency.
        keys (list): List of keys to replace the elements in `step`. The length of `keys` should be
                     at least as long as the number of unique elements in `step`.

    Returns:
        list: A new list where each element in `step` is replaced with a corresponding key from `keys`.

    Example:
        >>> replace_step_with_keys(['a', 'b', 'a', 'c', 'a', 'b'], ['key0', 'key1', 'key2'])
        ['key0', 'key1', 'key0', 'key2', 'key0', 'key1']
        # Here 'a' is replaced by 'key0', 'b' by 'key1', and 'c' by 'key2'.
        # As we can see the frequency order is kept intact after the map function.

    Notes:
        - Function is used to transform the original records distribution to a key distribution.
          Originally we created an integer distribution which we map the keys based on the frequency order as is specified from the adjust_or_create_key_dist function.
    """
    freq = Counter(step)
    sorted_values = [item for item, count in freq.most_common()]
    print(f"Sorted Value: {sorted_values}")
    value_to_key = {value: keys[i] for i, value in enumerate(sorted_values)}
    replaced_arr = [value_to_key[value] for value in step]

    return replaced_arr


def generate_step(arrival_rate, distribution, key_dist):
    """Generates a step in the key distribution in the stream simulation

    Args:
        arrival_rate (int): The arrival rate of keys in this step of the simulation
        distribution (class): The distribution class oject which generates keys based on
                              the distribution the keys are following in this step.
        key_dist (list): The list represents the frequency order of the keys in this step
                         that we want to simulate.


    Returns:
        list: The list of keys that were created in this step.
    """
    step = distribution.generate(arrival_rate)
    print(step)
    keys = replace_step_with_keys(step, key_dist)
    print(keys)
    return keys


def generate_stream(config, output_file, distribution):
    """Generates a key stream for the simulation. Runs the helper function generate_step
       for each step generation.


    Args:
        config (json): The json configuration of the simulation.
            "streams" (int): Number of discrete streams to generate.
            "steps" (int): Number of simulation steps.
            "number of keys" (int): Number of keys to use in the distribution.
            "arrival rate" (int): Number of keys per step.
            "distribution" (dict): Distribution configuration, including:
                "type" (str): Type of distribution, either "normal" or "uniform".
                "mean" (float): Mean for normal distribution (required if type is "normal").
                "stddev" (float): Standard deviation for normal distribution (required if type is "normal").
        output_file (str): Path to the output file where the stream will be written
        distribution (class): The distribution class oject which generates keys based on
                              the distribution the keys are following in this step.

    """
    stream = []
    # TODO: Further functionalities can be added here on the following topics:
    #           - Add more variations on how the key distribution changes in between steps
    #           - Add variation in arrival rate

    # key_dist originally contains the keys present in this simulation (e.g. ['key0' 'key1' 'key2]).
    key_dist = create_key_array(config["number of keys"], True)
    for i in range(config["steps"]):
        # key_dist now contains the frequency order that we wish the keys to follow in this step.
        # More on how this is handled in the description of the adjust_or_create_key_dist function.
        key_dist = adjust_or_create_key_dist(key_dist, i)

        print(f"Key dist: {key_dist}")
        step = generate_step(config["arrival rate"], distribution, key_dist)
        stream.append(" ".join(step))
    write_output(stream, output_file)


def generate_input(config, output_file):
    """Generates the input used in the simulator code.
       Creates multiple streams each saved in a different file for
       each discrete stream simulation.

    Args:
        config (json): The json configuration of the simulation.
            "streams" (int): Number of discrete streams to generate.
            "steps" (int): Number of simulation steps.
            "number of keys" (int): Number of keys to use in the distribution.
            "arrival rate" (int): Number of keys per step.
            "distribution" (dict): Distribution configuration, including:
                "type" (str): Type of distribution, either "normal" or "uniform".
                "mean" (float): Mean for normal distribution (required if type is "normal").
                "stddev" (float): Standard deviation for normal distribution (required if type is "normal").
        output_file (str): Path to the output file where the stream will be written

    Raises:
        This should never be reached.
        SystemExit: If the configuration is invalid or an unsupported distribution type is specified.


    Example:
        Given a config dictionary:
        {
            "streams": 3,
            "steps": 10,
            "number of keys": 3,
            "arrival rate": 10,
            "distribution": {
                "type": "uniform"
            }
        }
        and an output_file path "stream_output.txt",
        the function will create files "stream_output0.txt", "stream_output1.txt", "stream_output2.txt",
        each containing a stream of generated keys based on the uniform distribution.

    """

    dist_config = config["keygen"]

    # Validates the json configuration file for keygen
    validate_config(dist_config)

    dist_type = dist_config["distribution"]["type"]
    if dist_type == "normal":
        num_keys = dist_config["number of keys"]
        mean = dist_config["distribution"]["mean"]
        stddev = dist_config["distribution"]["stddev"]
        distribution = NormalDistribution(create_key_array(num_keys), mean, stddev)
    elif dist_type == "uniform":
        num_keys = dist_config["number of keys"]
        distribution = UniformDistribution(create_key_array(num_keys))
    else:
        # This should never be reached as it caught by the validate_config function
        sys.exit("An error occurred: Unsupported distribution type")

    for i in range(dist_config["streams"]):
        name, extension = os.path.splitext(output_file)
        generate_stream(dist_config, f"{name}{i}{extension}", distribution)


def main(config_file, output_file):
    config = load_config(config_file)
    generate_input(config, output_file)


if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent

    config_file = project_root / "config.json"
    output_file = project_root / "input/stream_output0.txt"

    main(config_file, output_file)
