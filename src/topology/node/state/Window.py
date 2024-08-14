class Window:
    """
    Represents a time window for tracking keys.

    Attributes:
        start_step (int): The starting step of the window.
        size (int): The size of the window in steps.
        keys (list): List of keys received within this window.
    """

    def __init__(self, start_step: int, window_size: int) -> None:
        """
        Initializes a Window instance with the given parameters.

        Args:
            start_step (int): The starting step of the window.
            window_size (int): The size of the window in steps.
        """
        self.start_step = start_step
        self.size = window_size
        self.keys = []

    def add_key(self, key: str) -> None:
        """
        Adds a key to the window's list of keys.

        Args:
            key (str): The key to be added.
        """
        self.keys.append(key)

    def is_full(self, current_step: int) -> bool:
        """
        Checks if the window is full based on the current step.

        Args:
            current_step (int): The current step in the simulation.

        Returns:
            bool: True if the window is full, False otherwise.
        """
        return current_step - self.start_step == self.size

    def is_expired(self, current_step: int) -> bool:
        """
        Checks if the window has expired based on the current step.

        Args:
            current_step (int): The current step in the simulation.

        Returns:
            bool: True if the window has expired, False otherwise.
        """
        return current_step - self.start_step > self.size

    def __repr__(self) -> str:
        """
        A string representation of the window.

        Returns:
            str: A formatted string showing the window's size, start step, and keys.
        """
        return (
            f"Window(size={self.size}, start_step={self.start_step}, keys={self.keys})"
        )
