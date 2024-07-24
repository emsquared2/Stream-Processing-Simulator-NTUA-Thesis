from typing import Any, List
from Node.Node import Node
from partition_strategies.PartitionStrategy import PartitionStrategy


class ShuffleGrouping(PartitionStrategy):
    """
    A partitioning strategy that distributes keys to nodes in a round-robin fashion.

    Attributes:
    - current_index (int): The index of the next node to receive a key.
    """

    def __init__(self):
        """
        Initializes the ShuffleGrouping strategy with the starting index.
        """
        self.current_index = 0

    def partition(self, keys: List[str], nodes: List[Node], buffers: dict) -> None:
        """
        Distributes keys to nodes in a round-robin manner.

        Each key is assigned to a node based on the current index, and then the
        index is updated to the next node in a circular fashion.

        Args:
        - keys (List[str]): The list of keys to be distributed.
        - nodes (List[Node]): The list of nodes to distribute the keys to.
        - buffers (dict): A dictionary where each key is an index corresponding
                          to a node, and the value is a list of keys to be buffered.
        """
        for key in keys:
            buffers[self.current_index].append(key)
            self.current_index = (self.current_index + 1) % len(nodes)