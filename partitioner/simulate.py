from Simulator import Simulator
from utils.load_file import load_file
from utils.load_sim_steps import load_steps_from_file

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

    # Read steps data from file
    steps_file = "../inputs/file.txt"
    steps_data = load_steps_from_file(steps_file)

    # Run the simulation
    simulator.sim(steps_data)

if __name__ == "__main__":
    main()
