from typing import Any, List
from partition_strategies.PartitionStrategy import PartitionStrategy


class ShuffleGrouping(PartitionStrategy):
    """
    A partitioning strategy that distributes keys in a round-robin fashion.

    Attributes:
    current_index (int): The index of the next node to receive a key.
    """

    def __init__(self):
        self.current_index = 0

    def partition(self, keys: List[str], nodes: List[Any], buffers: dict) -> None:
        """
        Distributes keys to nodes in a round-robin manner and buffers them.

        Args:
        keys (List[str]): The keys to be distributed.
        nodes (List[Any]): The nodes to distribute the keys to.
        buffers (dict): A buffer to hold keys before sending them to nodes.
        """
        for key in keys:
            buffers[self.current_index].append(key)
            self.current_index = (self.current_index + 1) % len(nodes)
