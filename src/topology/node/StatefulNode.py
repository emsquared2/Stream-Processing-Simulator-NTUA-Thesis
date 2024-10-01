from simulator.GlobalConfig import GlobalConfig
from .Node import Node
from utils.Logging import initialize_logging


class StatefulNode(Node):
    """
    Represents a stateful node in the simulation.

    Attributes:
        uid (int): Unique identifier for the node.
        stage_node_id: The stage local node identifier.
        type (str): The type of the node (stateful).
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): Complexity type used for computational cycle calculation.
        stage (Stage): The stage which the node is in.
        window_size (int): The size of the processing window.
        slide (int): The slide of the processing window.
        terminal (bool): Specifies if the current node is a
                             terminal (final stage) node.
        state (State): Class the represents the internal node State.
    """

    def __init__(
        self,
        uid: int,
        stage_node_id: int,
        node_type: str,
        throughput: int,
        stage,
        terminal: bool = False
    ) -> None:
        """
        Initializes the stateful node with the specified parameters.

        Args:
            uid (int): Unique identifier for the node.
            stage_node_id (int): Stage node identifier.
            throughput (int): Maximum computational cycles a node can
                              run per step.
            complexity_type (str): Complexity type used for computational cycle calculation.
            stage (Stage): The stage which the node is in.
            window_size (int): The size of the processing window.
            slide (int): The slide of the processing window.
            terminal (bool): Specifies if the current node is a
                             terminal (final stage) node.
        """
        super().__init__(uid, stage_node_id, node_type, throughput, stage)
        
        self.terminal = terminal    

        self.extra_dir = GlobalConfig.extra_dir

        # Initialize logging
        self.default_logger, self.node_logger, _ = initialize_logging(
            self.uid, self.extra_dir
        )

    def receive_and_process(self, keys: list, step: int) -> None:
        """
        Processes a list of keys and updates the node's internal state.

        Args:
            keys (list): List of keys to be processed.
            step (int): Current step in the simulation.
        """
        pass

    def emit_keys(self, keys: list, step: int) -> None:
        """Emits stage computed keys to next stage

        Args:
            keys (list): List of keys emitted from current
                         node to the next stage.
            step (int): The current simulation step.
        """
        pass

    def __repr__(self) -> str:
        """
        A string representation of the stateful node, including its ID and internal state.

        Returns:
            str: Description of the node.
        """
        pass