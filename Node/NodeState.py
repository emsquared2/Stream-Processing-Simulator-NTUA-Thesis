from typing import Counter
from Node.Window import Window

class NodeState:
    """
    A class to represent the state of a node in the simulation.

    Attributes:
    window_size (int): The size of the time window.
    slide (int): The sliding interval for the windows.
    node_id (int): The identifier for the node.
    received_keys (list): A list of keys received by the node.
    state (dict): A dictionary to track the state of keys.
    windows (dict): A dictionary to manage the windows.
    current_step (int): The current step in the simulation.
    minimum_step (int): The minimum step to consider for processing keys.
    """

    def __init__(self, window_size: int, slide: int, node_id: int) -> None:
        self.window_size = window_size
        self.slide = slide
        self.node_id = node_id
        
        self.received_keys = []
        self.state = {}
        self.windows = {}
        self.current_step = 0
        self.minimum_step = 0
        
    def update(self, keys: list, step: int) -> None:
        """
        Updates the node state with a list of keys and step.

        Args:
        keys (list): The keys received.
        step (int): The step at which the keys were received.
        """
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
        print(f"Node {self.node_id} received keys: {keys} at step: {step}")

    def update_windows(self, key: str, step: int) -> None:
        """
        Adds the key to the relevant windows.

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
        Processes and clears windows that have reached their window size.
        """
        for start_step, window in list(self.windows.items()):
            if window.is_full(self.current_step):
                self.process_window(window)
                del self.windows[start_step]

    def remove_expired_windows(self) -> None:
        """
        Removes windows that have expired.
        """
        for start_step, window in list(self.windows.items()):
            if window.is_expired(self.current_step):
                del self.windows[start_step]
                
    def remove_expired_keys(self) -> None:
        """
        Removes keys that have expired.
        """
        self.received_keys = [(key, step, max_step) for key, step, max_step in self.received_keys if self.current_step <= max_step]
        
    def process_window(self, window: Window) -> None:
        """
        Processes a full window and updates the node's state.

        Args:
        window (Window): The window to process.
        """
        print(f"\n\nProcessing {window}...\n\n")
        window_key_count = {}
        for key in window.keys:
            if key in window_key_count:
                window_key_count[key] += 1
            else:
                window_key_count[key] = 1

        # Example processing: just printing the window content
        for key, count in window_key_count.items():
            print(f"Processing key: {key} with count: {count}")

    def __repr__(self) -> str:
        key_counts = Counter([key for key, _, _ in self.received_keys])
        return (
            f"Node ID: {self.node_id}\n"
            f"Keys: {self.received_keys}\n"
            f"Key Counts: {dict(key_counts)}\n"
            f"Minimum Step: {self.minimum_step}\n"
            f"Current Step: {self.current_step}\n"
            f"Current Windows: {self.windows}"
        )
