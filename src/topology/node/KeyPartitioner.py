from typing import Optional, Dict, Any

# from ..stage.Stage import Stage
from .StatelessNode import StatelessNode
from partitioning_stategies.Hashing import Hashing
from partitioning_stategies.KeyGrouping import KeyGrouping
from partitioning_stategies.ShuffleGrouping import ShuffleGrouping


class KeyPartitioner(StatelessNode):
    """
    Represents a stateless node in the simulation.

    Attributes:
        uid (int): Unique identifier for the node.
        type (str): The type of the node (stateless).
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): Complexity type used for computational cycle calculation.
    """

    # TODO: Add strategy params
    def __init__(
        self,
        uid: int,
        stage_node_id: int,
        throughput: int,
        complexity_type: str,
        stage,
        partitioning_strategy: str,
        strategy_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initializes the stateless node with the specified parameters.

        Args:
            uid (int): Unique identifier for the node.
            throughput (int): Maximum computational cycles a node can run per step.
            complexity_type (str): Complexity type used for computational cycle calculation.
            partitioning_strategy (str): The name of the partitioning strategy.
        """
        super().__init__(uid, stage_node_id, throughput, complexity_type, stage)

        # TODO: Initialize strategy
        # Based on implementation of issue #9:
        # https://github.com/emsquared2/Stream-Processing-Simulator-NTUA-Thesis/issues/9
        # Initialize the partitioning strategy based on the strategy name.
        self.strategy = self._init_strategy(partitioning_strategy, strategy_params)

        # Initialize a buffer for each node of the next stage
        # to temporarily store keys
        self.buffers = {i: [] for i in range(self.stage.next_stage_len) if self.stage.next_stage_len > 0}

    def _init_strategy(self, strategy_name, strategy_params):
        """
        Initializes the partitioning strategy based on the provided name and parameters.

        Args:
        - strategy_name (str): The name of the partitioning strategy.
        - strategy_params (dict): Parameters for the partitioning strategy.

        Returns:
        - PartitionStrategy: An instance of the specified partitioning strategy.

        Raises:
        - ValueError: If the strategy name is not recognized.
        """
        if strategy_name == "shuffle_grouping":
            return ShuffleGrouping()
        elif strategy_name == "hashing":
            return Hashing()
        elif strategy_name == "key_grouping":
            prefix_length = strategy_params.get("prefix_length", 1)
            return KeyGrouping(prefix_length)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

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
        
        print(self.uid)
        if not self.stage.terminal_stage:
            # Partition the keys
            self.strategy.partition(keys, self.stage.next_stage.nodes, self.buffers)

            # Process buffered keys and send them to the nodes
            self.send_buffered_keys(step)


    def send_buffered_keys(self, step_count: int):
        """
        Sends buffered keys to their respective nodes and clears the buffers.

        Args:
        - step_count (int): The current step number in the simulation.
        """
        for node_id, keys in self.buffers.items():
            keys.append("step_update")  # Add a step update marker to the keys
            self.stage.next_stage.nodes[node_id].receive_and_process(
                keys, step_count
            )  # Send keys to the node
            self.buffers[node_id] = []  # Clear the buffer for the next step

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
