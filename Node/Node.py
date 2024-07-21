from Node.NodeState import NodeState

class Node:
    """
    A class to represent a node in the simulation.

    Attributes:
    node_id (int): The identifier for the node.
    internal_state (NodeState): The internal state of the node.
    """
    def __init__(self, node_id: int, window_size: int, slide: int) -> None:
        self.node_id = node_id
        self.internal_state = NodeState(window_size, slide, self.node_id)
       
    def receive(self, keys: list, step: int) -> None:
        """
        Receives a list of keys and updates the node's internal state.

        Args:
        keys (list): A list of keys to be processed by the node.
        step (int): The current step in the simulation.
        """
        self.internal_state.update(keys, step)
        

    def __repr__(self):
        return (
            f"Node {self.node_id} with:\n"
            f"\n{self.internal_state}\n"
            "--------------------"
        )

