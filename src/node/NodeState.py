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
        throughput (int): Number of keys per step that a node can process.
        received_keys (list[tuple[str, int, int]]): List of keys received, with their arrival step and max_step.
        state (dict[str, int]): Dictionary to track the state of keys.
        windows (dict[int, Window]): Dictionary to manage the time windows.
        current_step (int): The current step in the simulation.
        minimum_step (int): The minimum step to consider for processing keys.
    """

    def __init__(
        self, node_id: int, window_size: int, slide: int, throughput: int, complexity_type: str
    ) -> None:
        """
        Initializes the NodeState with the given parameters.

        Args:
            node_id (int): Unique identifier for the node.
            window_size (int): Size of the time window.
            slide (int): Sliding interval for the windows.
            throughput (int): Number of keys per step that a node can process.
        """
        self.window_size = window_size
        self.slide = slide
        self.node_id = node_id
        self.throughput = throughput

        self.complexity = create_complexity(complexity_type)

        self.received_keys: list[tuple[str, int, int]] = []
        self.state: dict[str, int] = {}
        self.windows: dict[int, Window] = {}
        self.current_step = 0
        self.minimum_step = 0

    def update(self, keys: list[str], step: int) -> None:
        """
        Updates the node state with new keys and the current step.

        Args:
            keys (list[str]): List of keys received.
            step (int): The current step in the simulation.
        """
        self.current_step = max(self.current_step, step)
        self.minimum_step = max(0, self.current_step - self.window_size)
        max_step = self.minimum_step + self.window_size

        for key in keys:
            # The "key_update" key is a special marker added at the end of each node's buffer during key partitioning.
            # It is used to indicate the current step when no other keys are sent to the node.
            if key != "step_update":
                # The max_step is used to determine when a key has expired.
                self.received_keys.append((key, step, max_step))
                self.update_windows(key, step)

        self.process_full_windows()
        self.remove_expired_windows()
        self.remove_expired_keys()
        # print(f"Node {self.node_id} received keys: {keys} at step: {step}")

    def update_windows(self, key: str, step: int) -> None:
        """
        Adds a key to all relevant windows.

        Args:
            key (str): The key to add.
            step (int): The step at which the key was received.
        """
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
        for start_step, window in list(self.windows.items()):
            if window.is_expired(self.current_step):
                del self.windows[start_step]

    def remove_expired_keys(self) -> None:
        """
        Removes keys that have expired based on their max_step.
        """
        self.received_keys = [
            (key, step, max_step)
            for key, step, max_step in self.received_keys
            if self.current_step <= max_step
        ]

    def process_window(self, window: Window) -> None:
        """
        Processes a full window and updates the node's state.

        Args:
            window (Window): The window to process.
        """
        window_key_count: dict[str, int] = {}
        cycles = 0 # old keys_processed

        for key in window.keys:
            if cycles >= self.throughput:
                break
            window_key_count[key] = window_key_count.get(key, 0) + 1
            cycles += self.complexity.calculate_cycles(len(window.keys))


        # Example processing: printing key counts
        # for key, count in window_key_count.items():
        #     print(f"Processing key: {key} with count: {count}")

    def __repr__(self) -> str:
        """
        A string representation of the node's state.

        Returns:
            str: A formatted string showing the node's ID, received keys, key counts, current step, minimum step, and windows.
        """
        key_counts = Counter(key for key, _, _ in self.received_keys)
        return (
            f"Node ID: {self.node_id}\n"
            f"Received Keys: {self.received_keys}\n"
            f"Key Counts: {dict(key_counts)}\n"
            f"Minimum Step: {self.minimum_step}\n"
            f"Current Step: {self.current_step}\n"
            f"Current Windows: {self.windows}"
        )
