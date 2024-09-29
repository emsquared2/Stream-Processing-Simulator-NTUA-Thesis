import random
from typing import List, Dict
from topology.node.Node import Node
from .PartitionStrategy import PartitionStrategy


class PowerOfTwoChoices(PartitionStrategy):
    """
    A partitioning strategy that uses two hash functions to assign keys to the least loaded node.
    The system keeps track of the assigned node for each key to maintain consistency.

    Attributes:
    - key_node_map (Dict[str, int]): Shared dictionary from the Stage that tracks the node assigned to each key.
    """

    def __init__(self, key_node_map: Dict[str, int]):
        """
        Initializes the PowerOfTwoChoices strategy, using the shared key-to-node map from the Stage.

        Args:
        - key_node_map (Dict[str, int]): Shared map from the Stage that tracks key-to-node assignments.
        """
        self.key_node_map = key_node_map

    def partition(self, keys: List[str], nodes: List[Node], buffers: dict) -> None:
        """
        Distributes keys using two hash functions, and assigns each key to the least loaded node.
        Tracks the node for each key to ensure consistency across multiple partition steps.

        Args:
        - keys (List[str]): The list of keys to be partitioned.
        - nodes (List[Node]): The list of nodes to distribute the keys to.
        - buffers (dict): A dictionary where each key is an index corresponding to a node,
                          and the value is a list of keys to be buffered.
        """
        num_nodes = len(nodes)

        for key in keys:
            if key in self.key_node_map:
                # If the key has already been assigned, send it to the same node
                assigned_node = self.key_node_map[key]
            else:
                # Calculate two candidate nodes using hash functions
                node1_index = hash(key) % num_nodes
                node2_index = hash(key + "salt") % num_nodes

                # Ensure the two candidates are different
                while node1_index == node2_index:
                    node2_index = hash(key + f"salt{random.random()}") % num_nodes

                # Get the load of the two candidate nodes
                load1 = nodes[node1_index].state.load()
                load2 = nodes[node2_index].state.load()

                # Choose the least loaded node
                if load1 <= load2:
                    assigned_node = node1_index
                else:
                    assigned_node = node2_index

                # Store the chosen node in the shared map
                self.key_node_map[key] = assigned_node

            # Add the key to the buffer for the selected node
            buffers[assigned_node].append(key)
