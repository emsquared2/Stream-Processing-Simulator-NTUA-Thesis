from Simulator import Simulator
from utils.utils import load_config, load_steps_from_file
from pathlib import Path


def main(config_file, steps_file):
    """
    Main function to configure and run the simulation.
    """

    # Load the configuration file
    config = load_config(config_file)

    # Extract simulator properties from the configuration
    num_nodes = config["simulator"]["number_of_nodes"]
    strategy_name = config["simulator"]["strategy"]["name"]
    strategy_params = {
        key: value for key, value in config["simulator"]["strategy"].items()
    }
    window_size = config["node"]["window_size"]
    slide = config["node"]["slide"]
    throughput = config["node"]["throughput"]

    # Initialize the simulator with the extracted properties
    simulator = Simulator(
        num_nodes, strategy_name, window_size, slide, throughput, strategy_params
    )

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
