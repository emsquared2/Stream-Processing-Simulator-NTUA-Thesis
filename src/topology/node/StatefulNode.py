from .Node import Node
from .state.State import State


class StatefulNode(Node):
    """
    Represents a stateful node in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        type (str): The type of the node (stateful).
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): Complexity type used for computational cycle calculation.
        window_size (int): The size of the processing window.
        slide (int): The slide of the processing window.
    """

    def __init__(
        self,
        node_id: int,
        throughput: int,
        complexity_type: str,
        window_size: int,
        slide: int,
        terminal: bool = False, #TODO: Update constructors calls
        extra_dir: str = None,
    ) -> None:
        """
        Initializes the stateful node with the specified parameters.

        Args:
            node_id (int): Unique identifier for the node.
            throughput (int): Maximum computational cycles a node can
                              run per step.
            complexity_type (str): Complexity type used for computational cycle calculation.
            window_size (int): The size of the processing window.
            slide (int): The slide of the processing window.
            terminal (bool): Specifies if the current node is a
                             terminal (final stage) node.
        """
        super().__init__(node_id, "stateful", throughput, complexity_type, extra_dir)
        self.window_size = window_size
        self.slide = slide
        self.terminal = terminal

        self.state = State(
            node_id, throughput, complexity_type, window_size, slide, extra_dir
        )

    def receive_and_process(self, keys: list, step: int) -> None:
        """
        Processes a list of keys and updates the node's internal state.

        Args:
            keys (list): List of keys to be processed.
            step (int): Current step in the simulation.
        
        Returns: 
        """
        processed_keys = self.state.update(keys, step, self.terminal)
        # print(processed_keys)
        if not self.terminal:
            processed_keys_flat = [item for sublist in processed_keys for item in sublist]
            self.emit_keys(processed_keys_flat)

    def emit_keys(self, keys: list[list]) -> None:
        """Emits stage computed keys to next stage

        Args:
            keys (list): List of keys emitted from current
                         node to the next stage.
        
        TODO: This currently just prints the keys to be emitted.
              When 
        """
        print(keys)

    def __repr__(self) -> str:
        """
        A string representation of the stateful node, including its ID and internal state.

        Returns:
            str: Description of the node.
        """
        return (
            f"\n--------------------\n"
            f"StatefulNode {self.node_id} with:\n"
            f"throughput: {self.throughput}\n"
            f"complexity type: {self.complexity_type}\n"
            f"window size: {self.window_size}\n"
            f"slide: {self.slide}\n"
            f"state:\n"
            f"{self.state}\n"
            f"--------------------"
        )
