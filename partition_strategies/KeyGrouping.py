from typing import Any, List
from partition_strategies.PartitionStrategy import PartitionStrategy

class KeyGrouping(PartitionStrategy):
    """
    A partitioning strategy that groups keys by a prefix and distributes them to nodes.

    Attributes:
    prefix_length (int): The length of the prefix used for grouping keys.
    group_map (dict): A mapping of key groups to nodes.
    """
    def __init__(self, prefix_length = 1):
        self.prefix_length = prefix_length
        self.group_map = {}  # Dictionary to map key groups to nodes

    def partition(self, keys: List[str], nodes: List[Any], buffers: dict) -> None:
        """
        Distributes keys to nodes based on their prefixes and buffers them.

        Args:
        keys (List[str]): The keys to be distributed.
        nodes (List[Any]): The nodes to distribute the keys to.
        buffers (dict): A buffer to hold keys before sending them to nodes.
        """
        for key in keys:
            group_key = key[:self.prefix_length]
            node_index = hash(group_key) % len(nodes)
            buffers[node_index].append(key)
            if group_key not in self.group_map:
                self.group_map[group_key] = node_index

    def get_node_index(self, key: str) -> int:
        group_key = key[:self.prefix_length]
        return self.group_map.get(group_key, -1)
