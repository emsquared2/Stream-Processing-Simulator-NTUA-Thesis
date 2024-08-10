import logging
import os
import time
from collections import Counter
from .Window import Window
from utils.utils import create_complexity


class NodeState:
    """
    Represents the state of a node in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        window_size (int): Size of the time window.
        slide (int): Sliding interval for the windows.
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): The complexity that the computation follows.
        received_keys (list[tuple[str, int, int]]): List of keys received, with their arrival step and max_step.
        state (dict[str, int]): Dictionary to track the state of keys.
        windows (dict[int, Window]): Dictionary to manage the time windows.
        current_step (int): The current step in the simulation.
        minimum_step (int): The minimum step to consider for processing keys.
        total_keys (int): Total keys received.
        total_processed (int): Total keys processed.
        total_expired (int): Total keys expired.
        total_cycles (int): Total number of processing cycles used.
    """

    def __init__(
        self,
        node_id: int,
        window_size: int,
        slide: int,
        throughput: int,
        complexity_type: str,
        extra_dir: str = None,
    ) -> None:
        """
        Initializes the NodeState with the given parameters.

        Args:
            node_id (int): Unique identifier for the node.
            window_size (int): Size of the time window.
            slide (int): Sliding interval for the windows.
            Number of keys per step that a node can process.
            complexity_type (str): The complexity that the computation follows.
        """
        self.node_id = node_id
        self.window_size = window_size
        self.slide = slide
        self.throughput = throughput
        self.complexity = create_complexity(complexity_type)

        self.received_keys: list[tuple[str, int, int]] = []
        self.state: dict[str, int] = {}
        self.windows: dict[int, Window] = {}
        self.current_step = 0
        self.minimum_step = 0

        self.total_keys = 0
        self.total_processed = 0
        self.total_expired = 0
        self.total_cycles = 0

        self.extra_dir = extra_dir

        self._initialize_logging()

    def _initialize_logging(self):
        """
        Initializes both the default and per-node logging setup.
        """
        # Get NodeState directory path
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Generate the timestamp
        timestamp = time.strftime("%Y%m%d%H%M%S")

        # Define log directory and create a subdirectory for the current timestamp
        log_dir = os.path.join(base_dir, "../../logs")
        if self.extra_dir:
            log_dir = os.path.join(log_dir, self.extra_dir, timestamp)
        os.makedirs(log_dir, exist_ok=True)

        # Create a default log file within the timestamped directory
        default_log_file = os.path.join(log_dir, "log_default.log")

        # Set up the default logger
        logging.basicConfig(
            filename=default_log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.default_logger = logging.getLogger("default_logger")

        # Create a log file specific to this node within the timestamped directory
        node_log_file = os.path.join(log_dir, f"log_node{self.node_id}.log")

        # Set up the per-node logger
        node_logger = logging.getLogger(f"Node_{self.node_id}")
        node_logger.setLevel(logging.DEBUG)  # Set to the desired logging level

        # Create a file handler for the node-specific logger
        node_handler = logging.FileHandler(node_log_file)
        node_handler.setLevel(logging.DEBUG)  # Set to the desired logging level

        # Create a common formatter
        formatter = logging.Formatter(
            "%(asctime)s - Node %(node_id)d - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        node_handler.setFormatter(formatter)

        # Add the handler to the per-node logger
        node_logger.addHandler(node_handler)

        # Store the per-node logger in the instance
        self.node_logger = node_logger

    def log_default_info(self, message):
        """
        Logs an info message to the default logger.

        Args:
            message (str): The message to log.
        """
        self.default_logger.info(message)

    def log_node_info(self, message):
        """
        Logs an info message with the node_id included to the per-node logger.

        Args:
            message (str): The message to log.
        """
        self.node_logger.info(message, extra={"node_id": self.node_id})

    def update(self, keys: list[str], step: int) -> None:
        """
        Updates the node state with new keys and the current step.

        Args:
            keys (list[str]): List of keys received.
            step (int): The current step in the simulation.
        """
        self.total_keys += len(keys)

        self.log_default_info(f"Updating node at step {step} with keys: {keys}")
        self.current_step = max(self.current_step, step)
        self.minimum_step = max(0, self.current_step - self.window_size)
        max_step = self.minimum_step + self.window_size

        for key in keys:
            if key != "step_update":
                self.received_keys.append((key, step, max_step))
                self.update_windows(key, step)

        self.process_full_windows()
        self.remove_expired_windows()
        self.remove_expired_keys()

    def update_windows(self, key: str, step: int) -> None:
        """
        Adds a key to all relevant windows.

        Args:
            key (str): The key to add.
            step (int): The step at which the key was received.
        """
        self.log_default_info(f"Updating windows for key: {key} at step: {step}")
        for start_step in range(self.minimum_step, self.current_step + 1, self.slide):
            if step - start_step <= self.window_size:
                if start_step not in self.windows:
                    self.windows[start_step] = Window(start_step, self.window_size)
                self.windows[start_step].add_key(key)

    def process_full_windows(self) -> None:
        """
        Processes and clears windows that have reached their size limit.
        """
        for start_step, window in list(self.windows.items()):
            if window.is_full(self.current_step):
                self.process_window(window)
                del self.windows[start_step]

    def remove_expired_windows(self) -> None:
        """
        Removes windows that have expired based on the current step.
        """
        self.log_default_info("Removing expired windows.")
        for start_step, window in list(self.windows.items()):
            if window.is_expired(self.current_step):
                del self.windows[start_step]

    def remove_expired_keys(self) -> None:
        """
        Removes keys that have expired based on their max_step.
        """
        self.log_default_info("Removing expired keys.")
        expired_keys_count = 0
        updated_received_keys = []

        for key, step, max_step in self.received_keys:
            if self.current_step <= max_step:
                updated_received_keys.append((key, step, max_step))
            else:
                expired_keys_count += 1

        self.received_keys = updated_received_keys
        self.total_expired += expired_keys_count

    def process_window(self, window: Window) -> None:
        """
        Processes a full window and updates the node's state.

        Args:
            window (Window): The window to process.
        """
        self.log_default_info(f"Processing window starting at step {window.start_step}")
        window_key_count: dict[str, int] = {}
        processed_keys = 0
        cycles = 0

        for key in window.keys:
            if cycles >= self.throughput:
                break
            processed_keys += 1
            window_key_count[key] = window_key_count.get(key, 0) + 1
            cycles += self.complexity.calculate_cycles(len(window.keys))

        self.log_default_info(f"Processed {cycles} computational cycles for window.")
        self.log_node_info(
            f"Step {self.current_step} - Processed {processed_keys} keys - Node load {(cycles*100)/self.throughput}%"
        )
        self.total_cycles += cycles
        self.total_processed += processed_keys

    def __repr__(self) -> str:
        """
        A string representation of the node's state.

        Returns:
            str: A formatted string showing the node's ID, received keys, key counts, current step, minimum step, and windows.
        """
        key_counts = Counter(key for key, _, _ in self.received_keys)

        report_message = (
            f"\n------------------------------------------\n"
            f"Node Report for Node ID: {self.node_id}\n"
            f"Total Keys Received: {self.total_keys}\n"
            f"Total Keys Processed: {self.total_processed}\n"
            f"Total Keys Expired: {self.total_expired}\n"
            f"Total Processing Cycles: {self.total_cycles}\n"
            f"Current Step: {self.current_step}\n"
            f"Minimum Step: {self.minimum_step}\n"
            f"Number of Active Windows: {len(self.windows)}\n"
            f"Number of Active Keys: {len(self.received_keys)}\n"
            f"------------------------------------------"
        )
        self.log_default_info(report_message)

        return (
            f"Node ID: {self.node_id}\n"
            f"Received Keys: {self.received_keys}\n"
            f"Key Counts: {dict(key_counts)}\n"
            f"Minimum Step: {self.minimum_step}\n"
            f"Current Step: {self.current_step}\n"
            f"Current Windows: {self.windows}\n"
            f"Total Keys Received: {self.total_keys}\n"
            f"Total Keys Processed: {self.total_processed}\n"
            f"Total Keys Expired: {self.total_expired}\n"
            f"Total Processing Cycles: {self.total_cycles}"
        )
