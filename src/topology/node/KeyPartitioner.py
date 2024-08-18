from typing import Optional, Dict, Any

from .StatelessNode import StatelessNode
from partitioning_stategies.Hashing import Hashing
from partitioning_stategies.KeyGrouping import KeyGrouping
from partitioning_stategies.ShuffleGrouping import ShuffleGrouping


class KeyPartitioner(StatelessNode):
    """
    Represents a stateless node in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        type (str): The type of the node (stateless).
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): Complexity type used for computational cycle calculation.
    """

    # TODO: Add strategy params
    def __init__(
        self,
        node_id: int,
        throughput: int,
        complexity_type: str,
        partitioning_strategy: str,
        strategy_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initializes the stateless node with the specified parameters.

        Args:
            node_id (int): Unique identifier for the node.
            throughput (int): Maximum computational cycles a node can run per step.
            complexity_type (str): Complexity type used for computational cycle calculation.
            partitioning_strategy (str): The name of the partitioning strategy.
        """
        super().__init__(node_id, "stateless", throughput, complexity_type)

        # TODO: Initialize strategy
        # Based on implementation of issue #9:
        # https://github.com/emsquared2/Stream-Processing-Simulator-NTUA-Thesis/issues/9
        # Initialize the partitioning strategy based on the strategy name.
        self.strategy = self._init_strategy(partitioning_strategy, strategy_params)

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
        pass

    def __repr__(self) -> str:
        """
        A string representation of the stateless node.

        Returns:
            str: Description of the node.
        """
        return (
            f"\n--------------------\n"
            f"StatelessNode {self.node_id} with:\n"
            f"throughput: {self.throughput}\n"
            f"complexity type: {self.complexity_type}\n"
            f"--------------------"
        )
