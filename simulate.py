from Simulator import Simulator
from utils.load_file import load_file

def main():
    # Load configuration file
    config_file = "config.json"
    config = load_file(config_file)

    # Read simulator properties
    num_nodes = config["simulator"]["number_of_nodes"]
    strategy_name = config["simulator"]["strategy"]["name"]
    strategy_params = {key: value for key, value in config["simulator"]["strategy"].items()}
    window_size = config["node"]["window_size"]
    slide = config["node"]["slide"]

    simulator = Simulator(num_nodes, strategy_name, window_size, slide, strategy_params)

    # Simulate receiving data in steps
    steps_data = [
        ["apple", "apricot", "banana", "blueberry", "cherry"],
        ["apple", "date", "elderberry", "fig", "grape"],
        ["grapefruit", "banana", "apple", "kiwi", "lemon"],
        ["honeydew", "kiwi", "lemon", "mango", "nectarine"],
        ["orange", "nectarine", "papaya", "peach", "plum"],
        ["apple", "blueberry", "grape"]
    ]

    # Run the simulation
    simulator.sim(steps_data)

if __name__ == "__main__":
    main()
