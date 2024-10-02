from collections import Counter
from .BaseState import BaseState
from .Window import Window
from utils.Logging import log_default_info, log_node_info


class WorkerState(BaseState):
    """
    Represents the internal state of a Worker node in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        throughput (int): Maximum computational cycles a node can run per step.
        operation_type (str): Operation type used for computational cycle calculation.
        window_size (int): The size of the processing window.
        slide (int): The slide of the processing window.

        received_keys (list[tuple[str, int, int]]): List of keys received, with their arrival step and max_step.
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
        throughput: int,
        operation_type: str,
        window_size: int,
        slide: int,
    ) -> None:
        """
        Initializes the WorkerState with the given parameters.

        Args:
            node_id (int): Unique identifier for the node.
            throughput (int): Maximum computational cycles a node can run per step.
            operation_type (str): Operation type used for computational cycle calculation.
            window_size (int): The size of the processing window.
            slide (int): The slide of the processing window.
        """
        super().__init__(node_id, throughput, operation_type, window_size, slide)

        self.received_keys: list[tuple[str, int, int]] = []
        self.windows: dict[int, Window] = {}
        self.current_step = 0
        self.minimum_step = 0
        self.step_cycles = 0

        # Metrics
        self.total_keys = 0
        self.total_processed = 0
        self.total_expired = 0
        self.total_cycles = 0

    def update(self, keys: list[str], step: int, terminal: bool) -> list[list]:
        """
        Updates the state with new keys and the current step.

        Args:
            keys (list[str]): List of keys received.
            step (int): The current step in the simulation.
            terminal (bool): Specifies if the current node is a terminal node.

        Returns:
            list[list]: Returns the keys that will be emitted from the current window to the next stage (or aggregator).
                        If the node is terminal it returns an empty list.
        """
        self.total_keys += len(keys)

        log_default_info(
            self.default_logger,
            f"Updating node {self.node_id} at step {step} with keys: {keys}",
        )

        # Add check for new step to initialize again the step_cycles
        if self.current_step != step:
            self.step_cycles = 0

        self.current_step = max(self.current_step, step)
        self.minimum_step = max(0, self.current_step - self.window_size + 1)

        # TODO: Refactor max_step definition
        max_step = step + self.window_size + 3 * self.slide

        processed_keys, (processed_keys_count, step_cycles, overdue_keys) = self.process_full_windows(terminal)

        # Update total cycles used in current step
        self.step_cycles = step_cycles

        message = f"Step {self.current_step} - Processed {processed_keys_count} keys using {step_cycles} cycles - Node load {(step_cycles*100)/self.throughput}%"

        if overdue_keys:
            message += f" - Overdue keys: {overdue_keys}"

        log_default_info(
            self.default_logger,
            f"Node {self.node_id} Updating windows for keys: {keys} at step: {step}",
        )

        for key in keys:
            if key != "step_update" and step >= self.minimum_step:
                self.received_keys.append((key, step, max_step))
                self.update_windows(key, step)

        expired_keys = self.remove_expired_windows()

        if expired_keys:
            message += f" - Expired keys: {expired_keys}"

        log_node_info(
            self.node_logger,
            message,
            self.node_id,
        )

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
                self.windows[start_step] = Window(
                    start_step, self.window_size, self.slide
                )

        # Add the step keys to all non expired and non processable windows
        for st_step, window in list(self.windows.items()):
            if not window.is_expired(step) and not window.is_processable(step):
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
        step_cycles = self.step_cycles
        processed_keys = 0
        overdue_keys = 0

        for start_step, window in list(self.windows.items()):
            if window.is_processable(self.current_step):
                step_cycles, win_processed_keys, win_overdue_keys, window_keys = (
                    self.process_window(window, terminal, step_cycles)
                )
                processed_keys += win_processed_keys
                overdue_keys += win_overdue_keys
                if len(window.keys) == 0:
                    window_keys.append("finished")
                    del self.windows[start_step]
                emitted_keys.append((start_step, window_keys))

        return emitted_keys, (processed_keys, step_cycles, overdue_keys)

    def remove_expired_windows(self) -> None:
        """
        Removes windows that have expired based on the current step.
        """
        expired_windows = []
        expired_keys = 0
        for start_step, window in list(self.windows.items()):
            if window.is_expired(self.current_step):
                expired_windows.append(window)
                expired_keys += len(window.keys)
                self.total_expired += len(window.keys)
                del self.windows[start_step]

        if expired_windows:
            log_default_info(
                self.default_logger,
                f"Node {self.node_id} removed {len(window.keys)} expired keys.",
            )
            log_default_info(
                self.default_logger,
                f"Node {self.node_id} removed expired windows: {expired_windows} at step {self.current_step}",
            )

        return expired_keys

    def remove_expired_keys(self) -> None:
        """
        Removes keys that have expired based on their max_step.
        """
        updated_received_keys = []

        for key, start_step, max_step in self.received_keys:
            if self.current_step <= max_step:
                updated_received_keys.append((key, start_step, max_step))       

        self.received_keys = updated_received_keys

    def process_window(self, window: Window, terminal: bool, step_cycles: int) -> list:
        """
        Processes a full window and updates the state.

        Args:
            window (Window): The window to process.
            terminal (bool): Specifies if the current node is a terminal node.
            step_cycles (int): Computational cycles used so far in the current step.

        Returns:
            step_cycles (int): The computational cycles used so far in the current step.
            processed_keys (int): The number of keys that were processed in the window.
            overdue_keys (int): The total number of overdue keys in the window.
            list: The keys to be emitted from a window. If it is a terminal node it returns an empty list.
        """
        log_default_info(
            self.default_logger,
            f"Node {self.node_id} processing window starting at step {window.start_step}",
        )

        processed_keys, cycles, window_key_count = window.process(
            self.throughput, self.operation, step_cycles
        )

        step_cycles += cycles  # Cycles used so far in current step
        overdue_keys = window.keys  # Remaining unprocessed keys in this window

        message = f"Node {self.node_id} Processed {processed_keys} keys from window {window.start_step} using {cycles} cycles"
        if window.keys:
            message += f" - Overdue keys: {len(overdue_keys)}"

        log_default_info(
            self.default_logger,
            message,
        )

        self.total_cycles += cycles
        self.total_processed += processed_keys

        if terminal:
            return step_cycles, processed_keys, len(overdue_keys), []

        # window_key_count is a dictionary that tracks how many times each key has been
        # processed in the current window. If the operation is sorting or a nested loop,
        # we return a list of keys with each key repeated according to its count.
        # For aggregation operations, we return only the distinct keys.
        keys_list = (
            [key for key, count in window_key_count.items() for _ in range(count)]
            if self.operation.to_str() in {"Sorting", "NestedLoop"}
            else list(window_key_count.keys())
        )

        return step_cycles, processed_keys, len(overdue_keys), keys_list

    def load(self) -> int:
        """
        Computes the total load in terms of keys.
        Returns:
            int: The total number of keys in all active windows.
        """
        load = 0
        for window in self.windows.values():
            load += len(window.keys)

        return load

    def __repr__(self) -> str:
        """
        A string representation of the node's state.

        Returns:
            str: A formatted string showing the node's final state.
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
