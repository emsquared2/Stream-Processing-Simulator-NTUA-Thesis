from typing import List, Dict, Tuple
from topology.node.Node import Node
from .PartitionStrategy import PartitionStrategy
import random


class PartialKeyGrouping(PartitionStrategy):
    """
    A partitioning strategy that allows each key to be handled by two candidate nodes (key splitting).

    This strategy relaxes key grouping by dynamically choosing between two pre-selected candidate nodes
    for each key. The system selects the least loaded of the two candidate nodes during each call to
    the partition method.

    Attributes:
    - key_candidates (Dict[str, Tuple[int, int]]): Shared dictionary from the Stage class that maps
                                                   each key to its two pre-selected candidate nodes.
                                                   This ensures that all partitioners in the same stage
                                                   use the same key-to-candidate mapping.
    """

    def __init__(self, key_candidates: Dict[str, Tuple[int, int]]):
        """
        Initializes the PartialKeyGrouping strategy, using the shared key-to-candidates dictionary
        from the Stage class.

        Args:
        - key_candidates (Dict[str, Tuple[int, int]]): Shared dictionary from the Stage that tracks
          two candidate nodes for each key.
        """
        self.key_candidates = key_candidates

    def partition(self, keys: List[str], nodes: List[Node], buffers: dict) -> None:
        """
        Distributes keys using the Partial Key Grouping strategy.

        For each key, if it has not been seen before, two candidate nodes are selected
        using hash functions. These candidates are stored in the shared key_candidates dictionary
        for future partitioning decisions. When partitioning the key, the system dynamically selects
        the least loaded of the two candidate nodes to ensure load balancing. This decision is made
        dynamically every time the partition method is called.

        Args:
        - keys (List[str]): The list of keys to be partitioned.
        - nodes (List[Node]): The list of available nodes to distribute the keys to.
        - buffers (dict): A dictionary where each key is a node index, and the value is
                          a list of keys to be buffered for that node.
        """
        num_nodes = len(nodes)

        for key in keys:
            if key not in self.key_candidates:
                # If the key is new, select two candidate nodes using hash functions
                node1_index = hash(key) % num_nodes
                node2_index = hash(key + "salt") % num_nodes

                # Ensure the two candidates are different
                while node1_index == node2_index:
                    node2_index = hash(key + f"salt{random.random()}") % num_nodes

                # Store the two candidates for this key in the shared map
                self.key_candidates[key] = (node1_index, node2_index)
            else:
                # Retrieve the two candidates for this key from the shared map
                node1_index, node2_index = self.key_candidates[key]

            # Get the load of the two candidate nodes (active keys being processed)
            load1 = nodes[node1_index].state.load() + len(buffers[node1_index])
            load2 = nodes[node2_index].state.load() + len(buffers[node2_index])

            # Select the node with the least load
            if load1 <= load2:
                assigned_node = node1_index
            else:
                assigned_node = node2_index

            # Add the key to the buffer for the selected node
            buffers[assigned_node].append(key)
