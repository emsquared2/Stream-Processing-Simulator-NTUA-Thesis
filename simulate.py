from Simulator import Simulator
from utils.load_file import load_file

def main():
    
    # Load configuration file
    config_file = "config.json"
    config = load_file(config_file)
    
    # Read simulator properties
    num_nodes = config["simulator"]["number_of_nodes"]
    strategy_name = config["simulator"]["strategy"]
    prefix_length = config["simulator"]["prefix_length"]

    # Create simulator instance
    simulator = Simulator(num_nodes, strategy_name, prefix_length)

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
