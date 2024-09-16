from simulator.GlobalConfig import GlobalConfig
from .Node import Node
from .state.State import State
from utils.Logging import initialize_logging, log_default_info


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
        throughput: int,
        complexity_type: str,
        stage,
        window_size: int,
        slide: int,
        terminal: bool = False,
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
        super().__init__(
            uid, stage_node_id, "stateful", throughput, complexity_type, stage
        )
        self.window_size = window_size
        self.slide = slide
        self.terminal = terminal

        self.state = State(uid, throughput, complexity_type, window_size, slide)

        self.extra_dir = GlobalConfig.extra_dir

        # Initialize logging
        self.default_logger, self.node_logger = initialize_logging(
            self.uid, self.extra_dir
        )

    def receive_and_process(self, keys: list, step: int) -> None:
        """
        Processes a list of keys and updates the node's internal state.

        Args:
            keys (list): List of keys to be processed.
            step (int): Current step in the simulation.
        """
        log_default_info(
            self.default_logger, f"Node {self.uid} received keys: {keys} at step {step}"
        )

        processed_keys = self.state.update(keys, step, self.terminal)

        log_default_info(
            self.default_logger,
            f"Node {self.uid} terminal: {self.terminal}, processed_keys: {processed_keys}\n",
        )

        if not self.terminal:
            processed_keys_flat = [
                item for sublist in processed_keys for item in sublist
            ]
            self.emit_keys(processed_keys_flat, step)

    def emit_keys(self, keys: list, step: int) -> None:
        """Emits stage computed keys to next stage

        Args:
            keys (list): List of keys emitted from current
                         node to the next stage.
            step (int): The current simulation step.
        """
        self.stage.next_stage.nodes[self.stage_node_id].receive_and_process(keys, step)
        log_default_info(
            self.default_logger, f"Node {self.uid} emitted keys: {keys} at step {step}"
        )

    def __repr__(self) -> str:
        """
        A string representation of the stateful node, including its ID and internal state.

        Returns:
            str: Description of the node.
        """
        return (
            f"\n--------------------\n"
            f"StatefulNode {self.uid} with:\n"
            f"throughput: {self.throughput}\n"
            f"complexity type: {self.complexity_type}\n"
            f"window size: {self.window_size}\n"
            f"slide: {self.slide}\n"
            f"state:\n"
            f"{self.state}\n"
            f"--------------------"
        )
