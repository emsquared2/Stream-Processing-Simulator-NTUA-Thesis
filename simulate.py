from Simulator import Simulator
from utils.load_file import load_file


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

    # Define data to be simulated in each step
    steps_data = [
        ["apple", "apricot", "banana", "blueberry", "cherry"],
        ["apple", "date", "elderberry", "fig", "grape"],
        ["grapefruit", "banana", "apple", "kiwi", "lemon"],
        ["honeydew", "kiwi", "lemon", "mango", "nectarine"],
        ["orange", "nectarine", "papaya", "peach", "plum"],
        ["apple", "blueberry", "grape"],
    ]

    # Run the simulation with the provided data
    simulator.sim(steps_data)


if __name__ == "__main__":
    main()
