from typing import List
from node.Node import Node
from .PartitionStrategy import PartitionStrategy


class Hashing(PartitionStrategy):
    """
    A partitioning strategy that distributes keys based on their hash values.

    This class implements the PartitionStrategy interface by distributing keys to
    nodes according to the hash values of the keys.
    """

    def partition(self, keys: List[str], nodes: List[Node], buffers: dict) -> None:
        """
        Distributes keys to nodes based on their hash values.

        The method computes the hash of each key, determines the appropriate node
        based on the hash value, and appends the key to the corresponding buffer.

        Args:
        keys (List[str]): The keys to be distributed.
        nodes (List[Node]): The nodes to distribute the keys to.
        buffers (dict): A dictionary where each key is an index corresponding
                        to a node, and the value is a list of keys to be buffered.
        """
        for key in keys:
            node_index = hash(key) % len(nodes)
            buffers[node_index].append(key)
