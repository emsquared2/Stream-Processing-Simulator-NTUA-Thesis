from typing import Optional, Dict, Any

from topology.Topology import Topology
from partitioner.Hashing import Hashing
from partitioner.KeyGrouping import KeyGrouping
from partitioner.ShuffleGrouping import ShuffleGrouping
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
        self.nodes = self._select_stage_1_nodes()

        # Initialize a buffer for each node to temporarily store keys
        self.buffers = {i: [] for i in range(len(self.nodes))}

        # Initialize the partitioning strategy based on the strategy name
        self.strategy = self._init_strategy(strategy_name, strategy_params)

    def _select_stage_1_nodes(self):
        """
        Selects the nodes from the stage with id '1'.

        Returns:
        - list: A list of nodes from the stage with id '1'.
        """
        for stage in self.topology.stages:
            if stage.id == 1:
                return stage.nodes
        raise ValueError("Stage with id '1' not found in the topology.")

    def _init_strategy(self, strategy_name, strategy_params):
        """
        Initializes the partitioning strategy based on the provided name and parameters.

        Args:
        - strategy_name (str): The name of the partitioning strategy.
        - strategy_params (dict): Parameters for the partitioning strategy.

        Returns:
        - PartitionStrategy: An instance of the specified partitioning strategy.

        Raises:
        - ValueError: If the strategy name is not recognized.
        """
        if strategy_name == "shuffle_grouping":
            return ShuffleGrouping()
        elif strategy_name == "hashing":
            return Hashing()
        elif strategy_name == "key_grouping":
            prefix_length = strategy_params.get("prefix_length", 1)
            return KeyGrouping(prefix_length)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def sim(self, steps_data):
        """
        Simulates the reception and processing of keys across multiple steps.

        Args:
        - steps_data (list): A list of lists, where each sublist contains keys received in a step.
        """
        for step_count, step_keys in enumerate(steps_data):
            # Partition the keys
            self.strategy.partition(step_keys, self.nodes, self.buffers)

            # Process buffered keys and send them to the nodes
            self.send_buffered_keys(step_count)

        # Print the final state of all nodes
        self.report()

    def send_buffered_keys(self, step_count):
        """
        Sends buffered keys to their respective nodes and clears the buffers.

        Args:
        - step_count (int): The current step number in the simulation.
        """
        for node_id, keys in self.buffers.items():
            keys.append("step_update")  # Add a step update marker to the keys
            self.nodes[node_id].receive_and_process(
                keys, step_count
            )  # Send keys to the node
            self.buffers[node_id] = []  # Clear the buffer for the next step

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
        for node in self.nodes:
            print(node)  # Print the state of each node
