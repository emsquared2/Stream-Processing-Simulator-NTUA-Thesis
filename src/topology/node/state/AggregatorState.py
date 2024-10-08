from typing import Dict, List, Tuple
from .BaseState import BaseState
from .Window import Window
from utils.Logging import log_default_info, log_node_info


class AggregatorState(BaseState):
    """
    Represents the state of an AggregatorNode in the simulation.

    Attributes:
        node_id (int): Unique identifier for the node.
        throughput (int): Maximum computational cycles a node can run per step.
        operation_type (str): Operation type used for computational cycle calculation.
        window_size (int): The size of the processing window.
        slide (int): The slide of the processing window.
        stage_operation (str): The operation simulated by the stage where state's node is located in.
        stage_nodes_count (int): Total number of nodes in the stage.
        windows (Dict[int, Tuple[Window, List[bool]]]): Dictionary to manage windows.

        current_step (int): The current step in the simulation.
        minimum_step (int): The minimum step to consider for processing keys.

        total_processed (int): Total keys processed.
        total_expired (int): Total expired_keys.
        total_cycles (int): Total number of processing cycles used.
    """

    def __init__(
        self,
        node_id: int,
        throughput: int,
        operation_type: str,
        window_size: int,
        slide: int,
        stage_operation: str,
        stage_nodes_count: int,
    ) -> None:
        """
        Initializes the NodeState with the given parameters.
        Args:
            node_id (int): Unique identifier for the node.
            throughput (int): Maximum computational cycles a node can run per step.
            operation_type (str): Operation type used for computational cycle calculation.
            window_size (int): The size of the processing window.
            slide (int): The slide of the processing window.
            stage_operation (str): The operation simulated by the stage where state's node is located in.
            stage_nodes_count (int): Total number of nodes in the stage.
        """
        super().__init__(node_id, throughput, operation_type, window_size, slide)
        self.stage_nodes_count = stage_nodes_count
        self.stage_operation = stage_operation

        self.windows: Dict[int, Tuple[Window, List[bool]]] = {}
        self.current_step = 0
        self.minimum_step = 0

        # Metrics
        self.total_processed = 0
        self.total_expired = 0
        self.total_cycles = 0

    def update(
        self,
        keys: Dict[int, List[Dict[str, int]]],
        step: int,
        terminal: bool,
        sender_stage_id: int,
    ) -> list[list]:
        """
        Updates the node state with new keys and the current step.
        Args:
            keys (Dict[int, List[Dict[str, int]]]): List of keys received along with their count and their window start_step.
            step (int): The current step in the simulation.
            terminal (bool): Specifies if the current node is a terminal node.
            sender_stage_id (int): The sender's id in the stage.
        Returns:
            list[list]: Returns the keys that will be emitted from the current window to the next stage.
                        If the node is terminal it returns an empty list.
        """

        self.current_step = max(self.current_step, step)
        self.minimum_step = max(0, self.current_step - self.window_size + 1)

        log_default_info(
            self.default_logger,
            f"Node {self.node_id} Updating windows for keys: {keys} at step: {step}",
        )

        if step >= self.minimum_step:
            for window_start_step, key_count_list in keys.items():
                for key_count_dict in key_count_list:
                    for key, count in key_count_dict.items():
                        if key == "finished":
                            self.update_boolean_for_window(
                                window_start_step, sender_stage_id
                            )
                        else:
                            self.update_windows(key, count, step, window_start_step)

        log_default_info(
            self.default_logger,
            f"Updating node {self.node_id} at step {step} with keys: {keys}",
        )
        processed_keys = self.process_full_windows(terminal)

        self.remove_expired_windows()

        log_default_info(
            self.default_logger,
            f"Node {self.node_id} windows at step {step}: {self.windows}\n",
        )
        return processed_keys

    def update_boolean_for_window(self, window_start_step: int, sender_id: int) -> None:
        """
        Updates the boolean list at sender_id index for the specified window without modifying the window itself.
        Args:
            window_start_step (int): The step at which the window started.
            sender_id (int): The index in the boolean list representing the sender.
        """

        if window_start_step in self.windows:
            _, boolean_list = self.windows[window_start_step]

            # Update the boolean list at the sender_id index
            boolean_list[sender_id] = True

    def update_windows(
        self, key: str, count: int, step: int, window_start_step: int
    ) -> None:
        """
        Adds a key to window state.

        Args:
            key (str): The key to add.
            count (int): The number of key's occurrences.
            step (int): The step at which the key was received.
            window_start_step (int): The step at which the window started.
        """

        if window_start_step not in self.windows:
            window = Window(window_start_step, self.window_size, self.slide)
            self.windows[window_start_step] = (
                window,
                [False] * self.stage_nodes_count,
            )

        window, _ = self.windows[window_start_step]
        if not window.is_expired(step):
            for _ in range(count):
                window.add_key(key)

    def process_full_windows(self, terminal: bool) -> list[list]:
        """
        Processes and clears windows that have reached their size limit or finished their processing.
        Args:
            terminal (bool): Specifies if the current node is a terminal node.
        Returns:
            list[list]: Returns all the keys to be emitted to the next stage from each full window.
        """
        emitted_keys = []
        step_cycles = 0
        processed_keys = 0
        overdue_keys = 0

        for start_step, (window, finished) in list(self.windows.items()):
            if window.is_processable(self.current_step) and all(finished):
                step_cycles, win_processed_keys, win_overdue_keys, window_keys = (
                    self.process_window(window, terminal, step_cycles)
                )
                processed_keys += win_processed_keys
                overdue_keys += win_overdue_keys
                if len(window.keys) == 0:
                    del self.windows[start_step]
                emitted_keys.append((start_step, window_keys))

        message = f"Step {self.current_step} - Processed {processed_keys} keys using {step_cycles} cycles - Node load {(step_cycles*100)/self.throughput}%"

        if overdue_keys:
            message += f" - Overdue keys: {overdue_keys}"

        log_node_info(
            self.node_logger,
            message,
            self.node_id,
        )

        return emitted_keys

    def process_window(self, window: Window, terminal: bool, step_cycles: int) -> list:
        """
        Processes a full window and updates the node's state.
        Args:
            window (Window): The window to process.
            terminal (bool): Specifies if the current node is a terminal node.
            step_cycles (int): Computational cycles used so far in the current step.
        Returns:
            int: The computational cycles used so far in the current step.
            list: The keys to be emitted from a window. If it is a terminal node it returns an empty list.
        """
        log_default_info(
            self.default_logger,
            f"Node {self.node_id} processing window starting at step {window.start_step}",
        )

        processed_keys, cycles, window_key_count = window.process(
            self.throughput, self.operation, step_cycles
        )

        step_cycles += cycles
        overdue_keys = window.keys
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

        keys_list = (
            [key for key, count in window_key_count.items() for _ in range(count)]
            if self.stage_operation in {"Sorting", "NestedLoop"}
            else list(window_key_count.keys())
        )

        return step_cycles, processed_keys, len(overdue_keys), keys_list

    def remove_expired_windows(self) -> None:
        """
        Removes windows that have expired based on the current step.
        """
        expired_windows = []
        for start_step, (window, _) in list(self.windows.items()):
            if window.is_expired(self.current_step):
                expired_windows.append(window)
                self.total_expired += len(window.keys)
                log_default_info(
                    self.default_logger,
                    f"Node {self.node_id} removed {len(window.keys)} expired keys: {window.keys}",
                )
                del self.windows[start_step]

        if expired_windows:
            log_default_info(
                self.default_logger,
                f"Node {self.node_id} removed expired windows: {expired_windows} at step {self.current_step}",
            )

    def __repr__(self) -> str:
        """
        A string representation of the node's state.
        Returns:
            str: A formatted string showing the node's final state.
        """
        report_message = (
            f"\n------------------------------------------\n"
            f"Node Report for Node ID: {self.node_id}\n"
            f"Total Keys Processed: {self.total_processed}\n"
            f"Total Keys Expired: {self.total_expired}\n"
            f"Total Processing Cycles: {self.total_cycles}\n"
            f"Current Step: {self.current_step}\n"
            f"Minimum Step: {self.minimum_step}\n"
            f"Number of Active Windows: {len(self.windows)}\n"
            f"------------------------------------------"
        )
        log_default_info(self.default_logger, report_message)
        return (
            f"Node ID: {self.node_id}\n"
            f"Minimum Step: {self.minimum_step}\n"
            f"Current Step: {self.current_step}\n"
            f"Current Windows: {self.windows}\n"
            f"Total Keys Processed: {self.total_processed}\n"
            f"Total Keys Expired: {self.total_expired}\n"
            f"Total Processing Cycles: {self.total_cycles}"
        )
