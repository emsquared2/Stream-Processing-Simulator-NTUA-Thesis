from .Node import Node

class StatelessNode(Node):
    """
    Represents a stateless node in the simulation.

    Attributes:
        uid (int): Unique identifier for the node.
        stage_node_id: The stage local node identifier.
        type (str): The type of the node (stateless).
        throughput (int): Maximum computational cycles a node can run per step.
        stage (Stage): The stage which the node is in.
    """

    # TODO: Add strategy params
    def __init__(self, uid: int, stage_node_id: int, throughput: int, stage) -> None:
        """
        Initializes the stateless node with the specified parameters.

        Args:
            uid (int): Unique identifier for the node.
            stage_node_id (int): Stage node identifier.
            throughput (int): Maximum computational cycles a node can
                              run per step.
            stage (Stage): The stage which the node is in.
        """
        super().__init__(uid, stage_node_id, "stateless", throughput, stage)

    def receive_and_process(self, keys: list, step: int) -> None:
        """
        Processes a list of keys (no internal state update as it is stateless).

        Args:
            keys (list): List of keys to be processed.
            step (int): Current step in the simulation.
        """
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
            f"--------------------"
        )
