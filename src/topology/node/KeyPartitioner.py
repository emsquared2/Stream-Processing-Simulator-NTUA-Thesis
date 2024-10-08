from typing import Optional, Dict, Any

from simulator.GlobalConfig import GlobalConfig
from utils.Logging import initialize_logging, log_default_info

from .StatelessNode import StatelessNode
from partitioning_strategies.Hashing import Hashing
from partitioning_strategies.KeyGrouping import KeyGrouping
from partitioning_strategies.ShuffleGrouping import ShuffleGrouping
from partitioning_strategies.PowerOfTwoChoices import PowerOfTwoChoices
from partitioning_strategies.PartialKeyGrouping import PartialKeyGrouping


class KeyPartitioner(StatelessNode):
    """
    Represents a key partitioner stateless node in the simulation.

    Attributes:
        uid (int): Unique identifier for the node.
        stage_node_id: The stage local node identifier.
        type (str): The type of the node (stateless).
        throughput (int): Maximum computational cycles a node can
                          run per step.
        stage (Stage): The stage which the node is in.
        strategy (PartitionStrategy): The class the specifies the
                                      key partitioning strategy.
        buffers (dict): Buffers used to send the partitioned keys
                        to the next stage.
    """

    def __init__(
        self,
        uid: int,
        stage_node_id: int,
        throughput: int,
        stage,
        partitioning_strategy: str,
        strategy_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initializes the stateless node with the specified parameters.

        Args:
            uid (int): Global unique identifier for the node.
            stage_node_id: The stage local node identifier.
            throughput (int): Maximum computational cycles a node can
                              run per step.
            stage (Stage): The stage which the node is in.
            partitioning_strategy (str): The name of the partitioning
                                         strategy.
            strategy_params (dict): Parameters for the partitioning strategy.
        """
        super().__init__(uid, stage_node_id, throughput, stage)

        # Initialize partitioning strategy
        self.strategy = self._init_strategy(partitioning_strategy, strategy_params)

        # Initialize a buffer for each node of the next stage to temporarily store keys
        self.buffers = {
            i: []
            for i in range(self.stage.next_stage_len)
            if self.stage.next_stage_len > 0
        }

        self.extra_dir = GlobalConfig.extra_dir

        # Initialize logging
        self.default_logger, self.node_logger, _ = initialize_logging(
            self.uid, self.extra_dir
        )

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
            hash_seed = strategy_params.get("hash_seed")
            return Hashing(hash_seed)
        elif strategy_name == "key_grouping":
            prefix_length = strategy_params.get("prefix_length", 1)
            return KeyGrouping(prefix_length)
        elif strategy_name == "potc":
            return PowerOfTwoChoices(self.stage.key_node_map)
        elif strategy_name == "pkg":
            return PartialKeyGrouping(self.stage.key_candidates)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def receive_and_process(self, keys: list, step: int) -> None:
        """
        Processes a list of keys (no internal state update as it is stateless).

        Args:
            keys (list): List of keys to be processed.
            step (int): Current step in the simulation.

        Note: As it a KeyPartitioner class it partitions the keys and sends
              them to the next simulator stage.
        """

        log_default_info(
            self.default_logger,
            f"Node {self.uid} received keys: {keys} at step {step}\n",
        )
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
            f"--------------------"
        )
