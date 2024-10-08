from .StatefulNode import StatefulNode
from .state.AggregatorState import AggregatorState
from utils.Logging import log_default_info


class AggregatorNode(StatefulNode):
    """
    Represents a node that performs an aggregation operation in the simulation.

    Inherits from the abstract Node class and sets the uid in the format 'stage_node_id_aggr'.
    Attributes:
        uid (int): Unique custom (stage_id + "_aggr") identifier for the node.
        stage_node_id: The stage local node identifier.
        type (str): The type of the node (stateful).
        throughput (int): Maximum computational cycles a node can run per step.
        operation_type (str): Operation type used for computational cycle calculation.
        stage (Stage): The stage to which the node belongs.
        window_size (int): The size of the processing window.
        slide (int): The slide of the processing window.
        stage_operation (str): The operation simulated by the stage where this node is located in.
        terminal (bool): Flag indicating wheather the node is terminal (final stage) or not.
        state (State): Class the represents the internal node State.

    """

    def __init__(
        self,
        stage_node_id: int,
        operation_type: str,
        stage,
        window_size: int,
        slide: int,
        stage_operation: str,
        terminal: bool = False,
    ) -> None:
        """
        Initializes an AggregatorNode with a custom uid and specified parameters.

        Args:
            stage_node_id: The stage local node identifier.
            operation_type (str): Operation type used for computational cycle calculation.
            stage (Stage): The stage to which the node belongs.
            window_size (int): The size of the processing window.
            slide (int): The slide of the processing window.
            stage_operation (str): The operation simulated by the stage where this node is located in.
            terminal (bool): Flag indicating wheather the node is terminal (final stage) or not.
        """
        # Construct the uid in the desired format
        self.uid = f"{stage_node_id}_aggr"

        self.operation_type = operation_type

        # Initialize the base class with the custom uid
        super().__init__(self.uid, stage_node_id, "Aggregator", 1000, stage, terminal)

        self.state = AggregatorState(
            self.uid,
            self.throughput,
            operation_type,
            window_size,
            slide,
            stage_operation,
            len(self.stage.nodes),
        )

    def receive_and_process(
        self, keys: dict[int, list[dict[str, int]]], step: int, sender_stage_node_id
    ) -> None:
        """
        Processes a list of keys and updates the node's internal state.

        Args:
            keys (dict): Dict of keys to be processed.
            step (int): Current step in the simulation.
            sender_stage_node_id: The sender stage node ID.
        """

        log_default_info(
            self.default_logger,
            f"Node {self.uid} received keys: {keys} at step {step} from node {sender_stage_node_id}",
        )

        processed_keys = self.state.update(
            keys, step, self.terminal, sender_stage_node_id
        )

        if not self.terminal:
            processed_keys_flat = [
                key for _, window_keys in processed_keys for key in window_keys
            ]
            self.emit_keys(processed_keys_flat, step)

    def emit_keys(self, keys: list, step: int) -> None:
        log_default_info(
            self.default_logger,
            f"Node {self.uid} emitting {keys} in step {step}",
        )
        self.stage.next_stage.nodes[0].receive_and_process(keys, step)

    def __repr__(self) -> str:
        """
        A string representation of the aggregator node.

        Returns:
            str: Description of the node.
        """
        return (
            f"\n--------------------\n"
            f"AggregatorNode {self.uid} with:\n"
            f"throughput: 1000\n"
            f"terminal: {self.terminal}\n"
            f"operation type: {self.operation_type}\n"
            f"state:\n"
            f"{self.state}\n"
            f"--------------------"
        )
