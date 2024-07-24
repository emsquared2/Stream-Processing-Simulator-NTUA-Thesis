from Simulator import Simulator
from utils.load_file import load_file
from utils.load_sim_steps import load_steps_from_file


def main():
    """
    Main function to configure and run the simulation.
    """

    # Load the configuration file
    config_file = "config.json"
    config = load_file(config_file)

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
    steps_file = "../input/stream_output0.txt"
    steps_data = load_steps_from_file(steps_file)

    # Run the simulation with the provided data
    simulator.sim(steps_data)


if __name__ == "__main__":
    main()
