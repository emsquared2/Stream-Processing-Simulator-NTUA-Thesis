from .StatefulNode import StatefulNode
from .state.AggregatorState import AggregatorState
from utils.Logging import log_default_info


class AggregatorNode(StatefulNode):
    """
    Represents a node for aggregation tasks in the simulation.

    Inherits from the abstract Node class and sets the uid in the format 'stage_node_id_aggr'.
    """

    def __init__(
        self,
        stage_node_id: int,
        complexity_type: str,
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
            throughput (int): Maximum computational cycles a node can run per step.
            stage (Stage): The stage which the node is in.
            stage_operation (str): The operation simulated by the stage where this node is 
                                   located in. 
        """
        # Construct the uid in the desired format
        self.uid = f"{stage_node_id}_aggr"

        # Initialize the base class with the custom uid
        super().__init__(self.uid, stage_node_id, "Aggregator", 1000, stage, terminal)

        self.state = AggregatorState(self.uid, self.throughput, complexity_type, window_size, slide, stage_operation, len(self.stage.nodes))


    def receive_and_process(
        self, keys: dict[int, list[dict[str, int]]], step: int, sender_stage_node_id
    ) -> None:
        """
        Process the keys for this aggregator node.

        Args:
            keys (dict): Dict of keys to be processed.
            step (int): Current step in the simulation.
            sender_stage_node_id: The sender stage node ID.
        """
        print(keys, step, sender_stage_node_id)

        log_default_info(
            self.default_logger,
            f"Node {self.uid} received keys: {keys} at step {step} from node {sender_stage_node_id}",
        )

        processed_keys = self.state.update(keys, step, self.terminal, sender_stage_node_id)

        if not self.terminal:
            processed_keys_flat = [
                    key for _, window_keys in processed_keys for key in window_keys
            ]
            self.emit_keys(processed_keys_flat, step)


    def emit_keys(self, keys: list, step: int) -> None:
        print(keys)
        log_default_info(
            self.default_logger,
            f"Node {self.uid} emitting {keys} in step {step}",
        )
        self.stage.next_stage.nodes[0].receive_and_process(keys, step)

    def is_expired(self, window_step: int, step: int):
        return step >= window_step + self.window_size + 3 * self.slide

    def process(self, key_count_list: list[tuple[str, int]]):
        print(key_count_list)
        cycles = 0
        emitting_keys = []

        log_default_info(
            self.default_logger,
            f"Node {self.uid} processing {key_count_list}",
        )

        for key, count in key_count_list.items():
            if key != "finished":
                cycles += self.complexity.calculate_cycles(count)
                emitting_keys.append(key)

        return cycles, emitting_keys

    def __repr__(self) -> str:
        """
        A string representation of the aggregator node.

        Returns:
            str: Description of the node.
        """
        return (
            f"\n--------------------\n"
            f"AggregatorNode {self.uid} with:\n"
            f"complexity type: {self.complexity_type}\n"
            f"state:\n"
            f"{self.state}\n"
            f"--------------------"
        )
