from collections import Counter
from .StatefulNode import StatefulNode
from .state.WorkerState import WorkerState
from utils.Logging import log_default_info


class WorkerNode(StatefulNode):
    """
    Represents a stateful node in the simulation.

    Attributes:
        uid (int): Unique identifier for the node.
        stage_node_id: The stage local node identifier.
        type (str): The type of the node (stateful).
        throughput (int): Maximum computational cycles a node can run per step.
        operation_type (str): Operation type used for computational cycle calculation.
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
        operation_type: str,
        stage,
        window_size: int,
        slide: int,
        terminal: bool = False,
        key_splitting: bool = False,
    ) -> None:
        """
        Initializes the stateful node with the specified parameters.

        Args:
            uid (int): Unique identifier for the node.
            stage_node_id (int): Stage node identifier.
            throughput (int): Maximum computational cycles a node can
                              run per step.
            operation_type (str): Operation type used for computational cycle calculation.
            stage (Stage): The stage which the node is in.
            window_size (int): The size of the processing window.
            slide (int): The slide of the processing window.
            terminal (bool): Specifies if the current node is a
                             terminal (final stage) node.
        """
        super().__init__(uid, stage_node_id, "Worker", throughput, stage, terminal)
        self.key_splitting = key_splitting

        self.state = WorkerState(uid, throughput, operation_type, window_size, slide)

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
            if self.key_splitting:
                # Initialize a dictionary to hold the count of keys for each window_step
                keys_dict = {}

                # Iterate over each window_step and the corresponding window_keys
                for window_step, window_keys in processed_keys:
                    # Use Counter to count occurrences of each key in window_keys
                    key_counts = Counter(window_keys)

                    # Convert the key counts into the required list of dicts format
                    keys_dict[window_step] = [
                        {key: count} for key, count in key_counts.items()
                    ]

                # Emit the transformed dictionary based on key splitting logic
                self.emit_keys(keys_dict, step)
            else:
                processed_keys_flat = [
                    key for _, window_keys in processed_keys for key in window_keys
                ]
                self.emit_keys(processed_keys_flat, step)

    def emit_keys(self, keys: list, step: int) -> None:
        """Emits stage computed keys to next stage

        Args:
            keys (list): List of keys emitted from current
                         node to the next stage.
            step (int): The current simulation step.
        """
        if self.key_splitting:
            print("Emitting", step, keys)
            self.stage.aggregator.receive_and_process(keys, step, self.stage_node_id)
        else:
            self.stage.next_stage.nodes[self.stage_node_id].receive_and_process(
                keys, step
            )

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
            f"state:\n"
            f"{self.state}\n"
            f"--------------------"
        )
