from abc import ABC, abstractmethod


class Node(ABC):
    """
    Represents an abstract base class for a node in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        type (str): The type of the node (stateful or stateless).
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): Complexity type used for computational cycle calculation.
    """

    def __init__(
        self,
        node_id: int,
        type: str,
        throughput: int,
        complexity_type: str,
        extra_dir: str = None,
    ) -> None:
        """
        Initializes the node with the specified parameters.

        Args:
            node_id (int): Unique identifier for the node.
            type (str): The type of the node (stateful or stateless)
            throughput (int): Maximum computational cycles a node can run per step.
            complexity_type (str): Complexity type used for computational cycle calculation.
        """
        self.node_id = node_id
        self.type = type
        self.throughput = throughput
        self.complexity_type = complexity_type
        self.extra_dir = extra_dir

    @abstractmethod
    def receive_and_process(self, keys: list, step: int) -> None:
        """
        Processes a list of keys and updates the node's internal state (in case of stateful node).

        This method must be implemented by subclasses.

        Args:
            keys (list): List of keys to be processed.
            step (int): Current step in the simulation.
        """
        pass
