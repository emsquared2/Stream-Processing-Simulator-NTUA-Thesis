from .Node import Node


class StatelessNode(Node):
    """
    Represents a stateless node in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        type (str): The type of the node (stateless).
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): Complexity type used for computational cycle calculation.
    """

    # TODO: Add strategy params
    def __init__(
        self,
        node_id: int,
        throughput: int,
        complexity_type: str,
        extra_dir: str = None,
    ) -> None:
        """
        Initializes the stateless node with the specified parameters.

        Args:
            node_id (int): Unique identifier for the node.
            throughput (int): Maximum computational cycles a node can run per step.
            complexity_type (str): Complexity type used for computational cycle calculation.
        """
        super().__init__(node_id, "stateless", throughput, complexity_type, extra_dir)

        # TODO: Initialize strategy
        # Based on implementation of issue #9:
        # https://github.com/emsquared2/Stream-Processing-Simulator-NTUA-Thesis/issues/9

    def receive_and_process(self, keys: list, step: int) -> None:
        """
        Processes a list of keys (no internal state update as it is stateless).

        Args:
            keys (list): List of keys to be processed.
            step (int): Current step in the simulation.
        """
        # TODO: Implementation specific to StatelessNode
        # Based on implementation of issue #9:
        # https://github.com/emsquared2/Stream-Processing-Simulator-NTUA-Thesis/issues/9
        pass

    def __repr__(self) -> str:
        """
        A string representation of the stateless node.

        Returns:
            str: Description of the node.
        """
        return (
            f"\n--------------------\n"
            f"StatelessNode {self.node_id} with:\n"
            f"throughput: {self.throughput}\n"
            f"complexity type: {self.complexity_type}\n"
            f"--------------------"
        )
