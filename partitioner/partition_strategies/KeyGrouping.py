from typing import Any, List
from Node.Node import Node
from partition_strategies.PartitionStrategy import PartitionStrategy


class KeyGrouping(PartitionStrategy):
    """
    A partitioning strategy that groups keys by a prefix and distributes them to nodes.

    Attributes:
    - prefix_length (int): The length of the prefix used for grouping keys.
    - group_map (dict): A mapping of key groups to node indices.
    """

    def __init__(self, prefix_length=1):
        """
        Initializes the KeyGrouping strategy with a specified prefix length.

        Args:
        - prefix_length (int): The length of the key prefix used for grouping. Defaults to 1.
        """
        self.prefix_length = prefix_length
        self.group_map = {}  # Maps key groups to node indices

    def partition(self, keys: List[str], nodes: List[Node], buffers: dict) -> None:
        """
        Distributes keys to nodes based on their prefix and buffers them.

        Each key is assigned to a node based on the hash of its prefix.

        Args:
        - keys (List[str]): The list of keys to be distributed.
        - nodes (List[Node]): The list of nodes to distribute the keys to.
        - buffers (dict): A dictionary where each key is a node index, and the value
                          is a list of keys buffered for that node.
        """
        for key in keys:
            group_key = key[: self.prefix_length]
            node_index = hash(group_key) % len(nodes)
            buffers[node_index].append(key)
            if group_key not in self.group_map:
                self.group_map[group_key] = node_index

    def get_node_index(self, key: str) -> int:
        """
        Retrieves the node index for a given key based on its prefix.

        Args:
        - key (str): The key for which to find the node index.

        Returns:
        - int: The index of the node assigned to the key group, or -1 if the group is not mapped.
        """
        group_key = key[: self.prefix_length]
        return self.group_map.get(group_key, -1)