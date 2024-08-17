from collections import Counter
from .Window import Window
from simulator.GlobalConfig import GlobalConfig
from utils.Logging import initialize_logging, log_default_info, log_node_info
from utils.utils import create_complexity


class State:
    """
    Represents the state of a node in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        throughput (int): Maximum computational cycles a node can run per step.
        complexity_type (str): Complexity type used for computational cycle calculation.
        window_size (int): The size of the processing window.
        slide (int): The slide of the processing window.

        received_keys (list[tuple[str, int, int]]): List of keys received, with their arrival step and max_step.
        state (dict[str, int]): Dictionary to track the state of keys.
        windows (dict[int, Window]): Dictionary to manage the time windows.
        current_step (int): The current step in the simulation.
        minimum_step (int): The minimum step to consider for processing keys.

        TODO: Re-evaluate metrics and how they are computed
        total_keys (int): Total keys received.
        total_processed (int): Total keys processed.
        total_expired (int): Total keys expired.
        total_cycles (int): Total number of processing cycles used.
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

        self.received_keys: list[tuple[str, int, int]] = []
        self.state: dict[str, int] = {}
        self.windows: dict[int, Window] = {}
        self.current_step = 0
        self.minimum_step = 0

        self.total_keys = 0
        self.total_processed = 0
        self.total_expired = 0
        self.total_cycles = 0

        self.extra_dir = GlobalConfig.extra_dir

        # Initialize logging
        self.default_logger, self.node_logger = initialize_logging(
            self.node_id, self.extra_dir
        )

    def update(self, keys: list[str], step: int, terminal: bool) -> list[list]:
        """
        Updates the node state with new keys and the current step.

        Args:
            keys (list[str]): List of keys received.
            step (int): The current step in the simulation.
            terminal (bool): Specifies if the current node 
                             is a terminal node.

        Returns:
            list[list]: Returns the keys that will be emitted 
                        from the current window to the next 
                        stage. 
                        If the node is terminal it returns an
                        empty list. 
        """
        self.total_keys += len(keys)

        log_default_info(
            self.default_logger, f"Updating node at step {step} with keys: {keys}"
        )
        self.current_step = max(self.current_step, step)
        self.minimum_step = max(0, self.current_step - self.window_size + 1)
        max_step = self.minimum_step + self.window_size

        for key in keys:
            if key != "step_update":
                self.received_keys.append((key, step, max_step))
                self.update_windows(key, step)

        processed_keys = self.process_full_windows(terminal)
        self.remove_expired_windows()
        self.remove_expired_keys()
        return processed_keys

    def update_windows(self, key: str, step: int) -> None:
        """
        Adds a key to all relevant windows.

        Args:
            key (str): The key to add.
            step (int): The step at which the key was received.
        """
        log_default_info(
            self.default_logger, f"Updating windows for key: {key} at step: {step}"
        )
        for start_step in range(self.minimum_step, self.current_step + 1, self.slide):
            if step - start_step <= self.window_size:
                if start_step not in self.windows:
                    self.windows[start_step] = Window(start_step, self.window_size)
                self.windows[start_step].add_key(key)

    def process_full_windows(self, terminal: bool) -> list[list]:
        """Processes and clears windows that have reached their size limit.

        Args:
            terminal (bool): Specifies if the current node
                             is a terminal node.

        Returns:
            list[list]: Returns all the keys to be emitted to
                        the next stage from each full window.
        """
        emitted_keys = []
        for start_step, window in list(self.windows.items()):
            if window.is_full(self.current_step):
                emitted_keys.append(self.process_window(window, terminal))
                # TODO: Re-examine based on issue #6: https://github.com/emsquared2/Stream-Processing-Simulator-NTUA-Thesis/issues/6
                del self.windows[start_step]
        return emitted_keys

    def remove_expired_windows(self) -> None:
        """
        Removes windows that have expired based on the current step.
        """
        log_default_info(self.default_logger, "Removing expired windows.")
        for start_step, window in list(self.windows.items()):
            if window.is_expired(self.current_step):
                del self.windows[start_step]

    def remove_expired_keys(self) -> None:
        """
        Removes keys that have expired based on their max_step.
        """
        log_default_info(self.default_logger, "Removing expired keys.")
        expired_keys_count = 0
        updated_received_keys = []

        for key, step, max_step in self.received_keys:
            if self.current_step <= max_step:
                updated_received_keys.append((key, step, max_step))
            else:
                expired_keys_count += 1

        self.received_keys = updated_received_keys
        self.total_expired += expired_keys_count

    def process_window(self, window: Window, terminal: bool) -> list:
        """
        Processes a full window and updates the node's state.

        Args:
            window (Window): The window to process.
            terminal (bool): Specifies if the current node
                             is a terminal node.
        
        Returns: 
            list: Returns in a list the keys to be emitted from a window.
                  If it is a terminal node it returns an empty list. 
        """
        log_default_info(
            self.default_logger,
            f"Processing window starting at step {window.start_step}",
        )

        processed_keys, cycles, window_key_count = window.process(
            self.throughput, self.complexity
        )

        log_default_info(
            self.default_logger, f"Processed {cycles} computational cycles for window."
        )
        log_node_info(
            self.node_logger,
            f"Step {self.current_step} - Processed {processed_keys} keys - Node load {(cycles*100)/self.throughput}%",
            self.node_id,
        )
        self.total_cycles += cycles
        self.total_processed += processed_keys
        # TODO: We can use window_key_count to aggregate/store the key_count for all processed keys

        if terminal:
            return []
        else: 
            return list(processed_keys_set)

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
        log_default_info(self.default_logger, report_message)

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
