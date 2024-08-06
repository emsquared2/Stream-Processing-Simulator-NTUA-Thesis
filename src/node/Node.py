from .NodeState import NodeState


class Node:
    """
    Represents a node in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        internal_state (NodeState): The internal state of the node.
    """

    def __init__(
        self, node_id: int, window_size: int, slide: int, throughput: int, complexity_type: str
    ) -> None:
        """
        Initializes the node with the specified parameters.

        Args:
            node_id (int): Unique identifier for the node.
            window_size (int): Size of the window for the internal state.
            slide (int): Sliding interval for the window.
            throughput (int): Throughput rate used in the internal state.
        """
        self.node_id = node_id
        self.internal_state = NodeState(self.node_id, window_size, slide, throughput, complexity_type)

    def receive(self, keys: list, step: int) -> None:
        """
        Processes a list of keys and updates the node's internal state.

        Args:
            keys (list): List of keys to be processed.
            step (int): Current step in the simulation.
        """
        self.internal_state.update(keys, step)

    def __repr__(self) -> str:
        """
        A string representation of the node, including its ID and internal state.

        Returns:
            str: Description of the node.
        """
        return (
            f"Node {self.node_id} with:\n"
            f"{self.internal_state}\n"
            "--------------------"
        )
