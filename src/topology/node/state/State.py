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
        windows (dict[int, Window]): Dictionary to manage the time windows.
        current_step (int): The current step in the simulation.
        minimum_step (int): The minimum step to consider for processing keys.

        TODO: Re-evaluate metrics and how they are computed
        total_keys (int): Total keys received.
        total_processed (int): Total keys processed.
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
        self.windows: dict[int, Window] = {}
        self.current_step = 0
        self.minimum_step = 0

        # Metrics
        self.total_keys = 0
        self.total_processed = 0
        self.total_cycles = 0

        self.extra_dir = GlobalConfig.extra_dir

        # Initialize logging
        self.default_logger, self.node_logger, _ = initialize_logging(
            self.node_id, self.extra_dir
        )

    def update(self, keys: list[str], step: int, terminal: bool) -> list[list]:
        """
        Updates the node state with new keys and the current step.

        Args:
            keys (list[str]): List of keys received.
            step (int): The current step in the simulation.
            terminal (bool): Specifies if the current node is a terminal node.

        Returns:
            list[list]: Returns the keys that will be emitted from the current window to the next stage.
                        If the node is terminal it returns an empty list.
        """
        self.total_keys += len(keys)

        log_default_info(
            self.default_logger,
            f"Updating node {self.node_id} at step {step} with keys: {keys}",
        )

        self.current_step = max(self.current_step, step)
        self.minimum_step = max(0, self.current_step - self.window_size + 1)
        max_step = self.minimum_step + self.window_size

        processed_keys = self.process_full_windows(terminal)

        log_default_info(
            self.default_logger,
            f"Node {self.node_id} Updating windows for keys: {keys} at step: {step}",
        )

        for key in keys:
            if key != "step_update":
                self.received_keys.append((key, step, max_step))
                self.update_windows(key, step)

        self.remove_expired_windows()
        self.remove_expired_keys()

        log_default_info(
            self.default_logger,
            f"Node {self.node_id} windows at step {step}: {self.windows}\n",
        )
        return processed_keys

    def update_windows(self, key: str, step: int) -> None:
        """
        Adds a key to all relevant windows.

        Args:
            key (str): The key to add.
            step (int): The step at which the key was received.
        """

        # Adjust start_step to align with the sliding windows
        start_step = (self.current_step // self.slide) * self.slide

        # Create any new windows needed based on side and start_step
        if 0 <= step - start_step < self.window_size:
            if start_step not in self.windows:
                self.windows[start_step] = Window(start_step, self.window_size)

        # Add the step keys to all the non expired windows
        for st_step, window in list(self.windows.items()):
            if not window.is_expired(step):
                self.windows[st_step].add_key(key)

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
        emitted_keys = []
        for start_step, window in list(self.windows.items()):
            if window.is_full(self.current_step):
                emitted_keys.append(self.process_window(window, terminal))
                del self.windows[start_step]
        return emitted_keys

    def remove_expired_windows(self) -> None:
        """
        Removes windows that have expired based on the current step.
        """
        expired_windows = []
        for start_step, window in list(self.windows.items()):
            if window.is_expired(self.current_step):
                expired_windows.append(window)
                del self.windows[start_step]

        if expired_windows:
            log_default_info(
                self.default_logger,
                f"Node {self.node_id} removed expired windows: {expired_windows} at step {self.current_step}",
            )

    def remove_expired_keys(self) -> None:
        """
        Removes keys that have expired based on their max_step.
        """
        log_default_info(self.default_logger, "Removing expired keys.")
        updated_received_keys = []

        for key, step, max_step in self.received_keys:
            if self.current_step <= max_step:
                updated_received_keys.append((key, step, max_step))

        self.received_keys = updated_received_keys

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
            f"Node {self.node_id} processing window starting at step {window.start_step}",
        )

        processed_keys, cycles, window_key_count = window.process(
            self.throughput, self.complexity
        )

        log_default_info(
            self.default_logger,
            f"Node {self.node_id} processed {cycles} computational cycles for window.",
        )
        message = (
            f"Step {self.current_step} - Processed {processed_keys} keys using {cycles} cycles - Overdue keys: {len(window.keys)} - Node load {(cycles*100)/self.throughput}%"
            if window.keys
            else f"Step {self.current_step} - Processed {processed_keys} keys using {cycles} cycles - Node load {(cycles*100)/self.throughput}%"
        )
        log_node_info(
            self.node_logger,
            message,
            self.node_id,
        )

        self.total_cycles += cycles
        self.total_processed += processed_keys
        # TODO: We can use window_key_count to aggregate/store the key_count for all processed keys

        # If there are overdue keys (i.e., keys left in the window), pass them to the next closest window
        overdue_keys = window.keys  # Remaining unprocessed keys in this window

        if overdue_keys:
            # Find the next closest window
            next_window_start_step = None
            for st_step in sorted(self.windows):
                if st_step > window.start_step:
                    next_window_start_step = st_step
                    break

            # If no window is found, default to the next window in the slide
            if next_window_start_step is None:
                next_window_start_step = window.start_step + self.slide

            # Create the next window if it doesn't exist
            if next_window_start_step not in self.windows:
                self.windows[next_window_start_step] = Window(
                    next_window_start_step, self.window_size
                )

            log_default_info(
                self.default_logger,
                f"Node {self.node_id} passing overdue keys: {overdue_keys} to window with start_step {next_window_start_step}",
            )

            # Add the overdue keys to the next window
            for key in overdue_keys:
                self.windows[next_window_start_step].add_key(key)

        if terminal:
            return []
        else:
            # The window_key_count is a dictionary that holds
            # how many times a type of key was processed in the
            # window. We can extract all the different keys that
            # were processed in this window as follows.
            # As we previously clarified that a stateful node
            # will "simulate" an aggregation function.
            return list(window_key_count.keys())

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
            f"Total Processing Cycles: {self.total_cycles}"
        )
