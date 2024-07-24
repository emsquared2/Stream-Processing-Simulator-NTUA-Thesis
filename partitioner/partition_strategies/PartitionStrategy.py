from abc import ABC, abstractmethod
from typing import List
from Node.Node import Node


class PartitionStrategy(ABC):
    """
    Abstract base class for defining partitioning strategies.

    This class serves as a blueprint for any specific partitioning strategy that
    distributes a set of keys among a list of nodes. It defines an abstract
    method that must be implemented by any subclass.

    Methods:
    - partition(keys: List[str], nodes: List[Node], buffers: dict) -> None:
        Abstract method that must be implemented in a subclass. It is intended
        to partition the given keys among the specified nodes using
        partitioning-related buffers.

    Attributes:
    - No specific attributes are defined in this abstract base class.
    """

    @abstractmethod
    def partition(self, keys: List[str], nodes: List[Node], buffers: dict) -> None:
        """
        Abstract method to partition a list of keys among a list of nodes.

        This method must be overridden by any concrete subclass that inherits from
        PartitionStrategy. It is responsible for the logic of distributing keys
        to nodes and handling any associated buffers.

        Parameters:
        - keys (List[str]): A list of keys to be partitioned.
        - nodes (List[Node]): A list of nodes among which the keys will be partitioned.
        - buffers (dict): A dictionary for any partitioning-related data or buffers.

        Returns:
        - None: This method does not return any value.
        """
        pass
