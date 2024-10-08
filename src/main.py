from keygen.KeyGenerator import KeyGenerator
from simulator.Simulator import Simulator
from simulator.GlobalConfig import GlobalConfig
from utils.utils import load_config, load_steps_from_file
import argparse
import os


def main(config_file, key_gen_file=None, stream_file=None, extra_dir=None):
    """
    Main function to configure and run the simulation.

    Args:
        config_file (str): The path to the simulation configuration file.
        key_gen_file (str): If provided it generates new key data to the
                            path specified by the parameter.
        stream_file (str): If provided it reads key data from the path specified
                           by the parameter
        extra_dir (str): Specifies the logging directory.
    """

    # Load the configuration file
    config = load_config(config_file)

    GlobalConfig.extra_dir = extra_dir

    # If the key_gen_file argument is defined, generate the key streams
    if key_gen_file:
        keygen = KeyGenerator(config["keygen"])
        keygen.generate_input(key_gen_file)

        # Prepare stream files to load
        steps_data = []
        for i in range(config["keygen"]["streams"]):
            name, extension = os.path.splitext(key_gen_file)
            stream_file = f"{name}{i}{extension}"
            steps_data.extend(load_steps_from_file(stream_file))
    # If stream_file is defined, use the provided key stream file
    elif stream_file:
        steps_data = load_steps_from_file(stream_file)

    # Extract topology configuration
    topology = config["topology"]

    # Initialize the simulator with the topology
    simulator = Simulator(topology)

    # Run the simulation with the provided data
    simulator.sim(steps_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simulation")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path of the configuration file",
    )
    parser.add_argument(
        "--key_gen",
        type=str,
        help="Path of the generated key stream file",
    )
    parser.add_argument(
        "--stream",
        type=str,
        help="Path of the pre-existing key stream file",
    )
    parser.add_argument(
        "--logs",
        type=str,
        default=None,
        help="Path of the directory for generated logs",
    )

    args = parser.parse_args()

    config_file = args.config
    key_gen_file = args.key_gen
    stream_file = args.stream
    extra_dir = args.logs

    if not key_gen_file and not stream_file:
        raise ValueError("Either --key_gen or --stream must be specified.")

    main(config_file, key_gen_file, stream_file, extra_dir)
