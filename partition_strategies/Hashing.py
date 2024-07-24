from typing import Any, List
from partition_strategies.PartitionStrategy import PartitionStrategy


class Hashing(PartitionStrategy):
    """
    A partitioning strategy that distributes keys based on their hash values.
    """

    def partition(self, keys: List[str], nodes: List[Any], buffers: dict) -> None:
        """
        Distributes keys to nodes based on their hash values and buffers them.

        Args:
        keys (List[str]): The keys to be distributed.
        nodes (List[Any]): The nodes to distribute the keys to.
        buffers (dict): A buffer to hold keys before sending them to nodes.
        """
        for key in keys:
            node_index = hash(key) % len(nodes)
            buffers[node_index].append(key)
