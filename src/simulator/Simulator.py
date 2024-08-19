from typing import Optional, Dict, Any

from topology.Topology import Topology
from utils.utils import validate_topology

# TODO: Refactor sim flow (_init_strategy, send_buffered_keys, etc.)


class Simulator:
    """
    A class to simulate the distribution and processing of keys across multiple nodes.

    Attributes:
    - num_nodes (int): The number of nodes in the simulation.
    - topology_config (dict): A dictionary representing the entire topology.
    - strategy (PartitionStrategy): The partitioning strategy used for distributing keys.
    - buffers (dict): A dictionary to buffer keys for each node before processing.
    """

    def __init__(
        self,
        num_nodes: int,
        topology_config: dict,
        strategy_name: str,
        strategy_params: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes a new Simulator instance with the given parameters.

        Args:
        - num_nodes (int): The number of nodes in the simulation.
        - topology (dict): A dictionary representing the entire topology.
        - strategy_name (str): The name of the partitioning strategy to use.
        - strategy_params (dict, optional): Additional parameters for the partitioning strategy.
        """

        # Validate the topology configuration
        validate_topology(topology_config)

        self.num_nodes = num_nodes

        # Initialize the topology
        self.topology = Topology(topology_config)

        # Select nodes from stage with id '1'
        self.input_partitioner = self._find_stage0_partioner()

        # # Initialize a buffer for each node to temporarily store keys
        # self.buffers = {i: [] for i in range(len(self.nodes))}

        # # Initialize the partitioning strategy based on the strategy name
        # self.strategy = self._init_strategy(strategy_name, strategy_params)

    def _find_stage0_partioner(self):
        """
        Selects the nodes from the stage with id '1'.

        Returns:
        - list: A list of nodes from the stage with id '1'.
        """
        for stage in self.topology.stages:
            if stage.id == 0:
                return stage.nodes[0]
        raise ValueError("Stage with id '0' not found in the topology.")

    def sim(self, steps_data):
        """
        Simulates the reception and processing of keys across multiple steps.

        Args:
        - steps_data (list): A list of lists, where each sublist contains keys received in a step.
        """

        for step_count, step_keys in enumerate(steps_data):
            self.input_partitioner.receive_and_process(step_keys, step_count)

        # Print the final state of all nodes
        self.report()

    def report(self):
        """
        Prints the final state of all nodes after the simulation.
        """
        final_state_message = """
------------------------
|                      |
| Final state of nodes |
|                      |
------------------------
"""
        print(final_state_message)
        for stage in self.topology.stages:
            for node in stage.nodes:
                print(node)  # Print the state of each node
