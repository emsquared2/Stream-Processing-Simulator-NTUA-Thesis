from src.keygen.KeyGenerator import KeyGenerator
from src.simulator.Simulator import Simulator
from src.simulator.GlobalConfig import GlobalConfig
from src.utils.utils import load_config, load_steps_from_file
import argparse
import os


def main(config_file, output_file, extra_dir=None):
    """
    Main function to configure and run the simulation.
    """

    # Load the configuration file
    config = load_config(config_file)

    # Generate the key streams using the updated configuration
    keygen = KeyGenerator(config["keygen"])
    keygen.generate_input(output_file)

    # Extract topology configuration
    topology = config["topology"]

    GlobalConfig.extra_dir = extra_dir

    # Initialize the simulator with the topology
    simulator = Simulator(topology)
    
    # Read steps data from all generated files
    steps_data = []
    for i in range(config["keygen"]["streams"]):
        name, extension = os.path.splitext(output_file)
        stream_file = f"{name}{i}{extension}"
        steps_data.extend(load_steps_from_file(stream_file))

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
        "--output",
        type=str,
        required=True,
        help="Path of the generated key stream file",
    )
    parser.add_argument(
        "--logs",
        type=str,
        default=None,
        help="Path of the directory generated logs",
    )

    args = parser.parse_args()

    config_file = args.config
    output_file = args.output
    extra_dir = args.logs

    main(config_file, output_file, extra_dir)


