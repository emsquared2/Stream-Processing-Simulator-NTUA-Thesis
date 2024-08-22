from Simulator import Simulator
from utils.utils import load_config, load_steps_from_file
from pathlib import Path


def main(config_file, steps_file):
    """
    Main function to configure and run the simulation.
    """

    # Load the configuration file
    config = load_config(config_file)

    # Extract topology configuration
    topology = config["topology"]

    # Initialize the simulator with the topology
    simulator = Simulator(topology)

    # Read steps data from file
    steps_data = load_steps_from_file(steps_file)

    # Run the simulation with the provided data
    simulator.sim(steps_data)


if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent

    config_file = project_root / "config.json"
    steps_file = project_root / "input/stream_output0.txt"
    main(config_file, steps_file)
