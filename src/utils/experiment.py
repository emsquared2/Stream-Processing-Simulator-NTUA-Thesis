from keygen.KeyGenerator import KeyGenerator
from simulator.Simulator import Simulator
from simulator.GlobalConfig import GlobalConfig
from utils.utils import (
    load_steps_from_file,
    load_config,
    update_config,
)
from utils.ConfigValidator import validate_topology


def run_experiment(config_file, output_file, extra_dir=None, **kwargs):
    """
    Run an experiment with specific parameters modified from the config file.

    Args:
        config_file (str): Path to the configuration file.
        output_file (str): Prefix for the output files where the generated keys will be saved.
        **kwargs: Parameters to be modified in the configuration file.
    """
    # Load the configuration configuration
    config = load_config(config_file)

    # Modify the configuration based on kwargs
    config = update_config(config, **kwargs)

    # Generate the key streams using the updated configuration
    keygen = KeyGenerator(config["keygen"])
    keygen.generate_input(output_file)

    # Extract topology configuration
    topology = config["topology"]

    # Validate the topology configuration
    validate_topology(topology)

    GlobalConfig.extra_dir = extra_dir

    # Initialize the simulator
    simulator = Simulator(topology)

    # Read steps data from all generated files
    steps_data = []
    for i in range(config["keygen"]["streams"]):
        stream_file = f"{output_file}{i}"
        steps_data.extend(load_steps_from_file(stream_file))

    # Run the simulation with the modified configuration
    simulator.sim(steps_data)
