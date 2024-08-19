from .Node import Node
# from ..stage.Stage import Stage


class StatelessNode(Node):
    """
    Represents a stateless node in the simulation.

    Attributes:
        uid (int): Unique identifier for the node.
        type (str): The type of the node (stateless).
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): Complexity type used for computational cycle calculation.
    """

    # TODO: Add strategy params
    def __init__(self, uid: int, stage_node_id: int, throughput: int, complexity_type: str, stage) -> None:
        """
        Initializes the stateless node with the specified parameters.

        Args:
            uid (int): Unique identifier for the node.
            stage_node_id (int): Stage node identifier.
            throughput (int): Maximum computational cycles a node can run per step.
            complexity_type (str): Complexity type used for computational cycle calculation.
        """
        super().__init__(uid, stage_node_id, "stateless", throughput, complexity_type, stage)

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
            f"StatelessNode {self.uid} with:\n"
            f"throughput: {self.throughput}\n"
            f"complexity type: {self.complexity_type}\n"
            f"--------------------"
        )
