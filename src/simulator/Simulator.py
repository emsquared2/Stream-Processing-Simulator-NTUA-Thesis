from typing import Optional, Dict, Any

from node.Node import Node
from partitioner.partition_strategies.Hashing import Hashing
from partitioner.partition_strategies.KeyGrouping import KeyGrouping
from partitioner.partition_strategies.ShuffleGrouping import ShuffleGrouping


class Simulator:
    """
    A class to simulate the distribution and processing of keys across multiple nodes.

    Attributes:
    - num_nodes (int): The number of nodes in the simulation.
    - window_size (int): The size of the time window for each node.
    - slide (int): The sliding interval for the windows.
    - throughput (int): The number of keys each node can process per step.
    - nodes (list): A list of Node instances.
    - strategy (PartitionStrategy): The partitioning strategy used for distributing keys.
    - buffers (dict): A dictionary to buffer keys for each node before processing.
    """

    def __init__(
        self,
        num_nodes: int,
        strategy_name: str,
        window_size: int,
        slide: int,
        throughput: int,
        strategy_params: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes a new Simulator instance with the given parameters.

        Args:
        - num_nodes (int): The number of nodes in the simulation.
        - strategy_name (str): The name of the partitioning strategy to use.
        - window_size (int): The size of the time window for each node.
        - slide (int): The sliding interval for the time windows.
        - throughput (int): The number of keys each node can process per step.
        - strategy_params (dict, optional): Additional parameters for the partitioning strategy.
        """
        self.num_nodes = num_nodes
        self.window_size = window_size
        self.slide = slide
        self.throughput = throughput

        # Create a list of Node instances
        self.nodes = [Node(i, window_size, slide, throughput) for i in range(num_nodes)]

        # Initialize a buffer for each node to temporarily store keys
        self.buffers = {i: [] for i in range(num_nodes)}

        # Initialize the partitioning strategy based on the strategy name
        self.strategy = self._init_strategy(strategy_name, strategy_params)

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
            self.nodes[node_id].receive(keys, step_count)  # Send keys to the node
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
