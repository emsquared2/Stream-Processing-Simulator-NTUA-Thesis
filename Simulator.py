from Node.Node import Node
from partition_strategies.Hashing import Hashing
from partition_strategies.KeyGrouping import KeyGrouping
from partition_strategies.ShuffleGrouping import ShuffleGrouping

class Simulator:
    """
    A class to simulate the distribution and processing of keys across multiple nodes.

    Attributes:
    num_nodes (int): The number of nodes in the simulation.
    window_size (int): The size of the time window.
    slide (int): The sliding interval for the windows.
    nodes (list): A list of Node instances.
    strategy (PartitionStrategy): The partitioning strategy used for distributing keys.
    buffers (dict): A dictionary to buffer keys for each node before sending.
    """
    
    def __init__(self, num_nodes, strategy_name, window_size, slide, strategy_params=None):
        """
        Initializes a new Simulator instance.

        Args:
        num_nodes (int): The number of nodes.
        strategy_name (str): The name of the partitioning strategy.
        window_size (int): The size of the time window.
        slide (int): The sliding interval for the windows.
        strategy_params (dict, optional): Additional parameters for the strategy.
        """
        self.num_nodes = num_nodes
        self.window_size = window_size
        self.slide = slide

        # Create the nodes with the given window size and slide
        self.nodes = [Node(i, window_size, slide) for i in range(num_nodes)]
        self.buffers = {i: [] for i in range(num_nodes)}

        # Initialize the strategy
        self.strategy = self._init_strategy(strategy_name, strategy_params)

    def _init_strategy(self, strategy_name, strategy_params):
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
        Simulates the receiving and processing of keys over a series of steps.

        Args:
        steps_data (list): A list of lists, where each sublist contains keys received in a step.
        """
        for step_count, step_keys in enumerate(steps_data):
            # Distribute keys to nodes based on the selected strategy
            self.strategy.partition(step_keys, self.nodes, self.buffers)
            
            # Send buffered keys to nodes
            self.send_buffered_keys(step_count)

        self.report()
        
    def send_buffered_keys(self, step_count):
        """
        Sends buffered keys to their respective nodes for processing.

        Args:
        step_count (int): The current step count.
        """
        for node_id, keys in self.buffers.items():
            self.nodes[node_id].receive(keys, step_count)
            self.buffers[node_id] = []  # Clear the buffer for the next step

    def report(self):
        """
        Prints the final state of all nodes.
        """
        final_state_message = \
"""
------------------------
|                      |
| Final state of nodes |
|                      |
------------------------
"""
        print(final_state_message)
        for node in self.nodes:
            print(node)
