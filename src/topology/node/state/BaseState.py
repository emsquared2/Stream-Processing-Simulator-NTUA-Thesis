from utils.utils import create_complexity
from simulator.GlobalConfig import GlobalConfig
from utils.Logging import initialize_logging


class BaseState:
    """
    An abstract class representing the state of a node.
    Attributes:
        node_id (int): Unique identifier for the node.
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
    ) -> None:
        """
        Initializes the NodeState with the given parameters.

        Args:
            node_id (int): Unique identifier for the node.
            throughput (int): Maximum computational cycles a node can run per step.
            complexity_type (str): Complexity type used for computational cycle calculation.
            window_size (int): The size of the processing window.
            slide (int): The slide of the processing window.
        """
        self.node_id = node_id
        self.throughput = throughput
        self.complexity = create_complexity(complexity_type)
        self.window_size = window_size
        self.slide = slide
        self.extra_dir = GlobalConfig.extra_dir

        # Initialize logging
        self.default_logger, self.node_logger, _ = initialize_logging(
            self.node_id, self.extra_dir
        )

    def update(self, keys, step, terminal):
        """
        Updates the node state with new keys and the current step.
        """
        pass

    def process_full_windows(self, terminal: bool) -> list[list]:
        """
        Processes and clears windows that have reached their size limit.

        Args:
            terminal (bool): Specifies if the current node
                             is a terminal node.

        Returns:
            list[list]: Returns all the keys to be emitted to
                        the next stage from each full window.
        """
        pass

    def remove_expired_windows(self) -> None:
        """
        Removes windows that have expired based on the current step.
        """
        pass
