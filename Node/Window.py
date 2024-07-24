class Window:
    """
    A class to represent a window of time for tracking keys.

    Attributes:
    start_step (int): The starting step of the window.
    size (int): The size of the window in steps.
    keys (list): The list of keys received within this window.
    """

    def __init__(self, start_step: int, window_size: int):
        self.start_step = start_step
        self.size = window_size
        self.keys = []

    def add_key(self, key: str):
        self.keys.append(key)

    def is_full(self, current_step: int):
        """
        Checks if the window is full based on the current step.
        """
        return current_step - self.start_step == self.size

    def is_expired(self, current_step: int):
        """
        Checks if the window is expired based on the current step.
        """
        return current_step - self.start_step > self.size

    def __repr__(self):
        return (
            f"Window(size={self.size}, start_step={self.start_step}, keys={self.keys})"
        )
