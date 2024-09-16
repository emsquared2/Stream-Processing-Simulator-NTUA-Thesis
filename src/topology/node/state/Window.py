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

    def process(self, throughput: int, complexity) -> tuple[int, int]:
        """
        Processes the keys in the window based on the throughput and complexity.
        Removes the processed keys from the window and returns the count of the processed keys.

        Args:
            throughput (int): Maximum computational cycles a node can run per step.
            complexity (Complexity): The complexity object to calculate computational cycles.

        Returns:
            tuple[int, int, dict[str, int]]: Number of keys processed, total cycles used, and the count of the processed keys.
        """
        cycles = 0
        processed_key_count: dict[str, int] = {}

        for key in self.keys:
            # Update processed_key_count
            processed_key_count[key] = processed_key_count.get(key, 0) + 1

            # Calculate the cycles required to process current keys
            cycles = self.compute_cost(processed_key_count, complexity)
            if cycles > throughput:
                # Stop processing if adding this key's cycles exceeds the throughput
                # Revert the increment made to processed_key_count for this key
                processed_key_count[key] -= 1
                if processed_key_count[key] == 0:
                    del processed_key_count[key]  # Remove key if occurrences is 0
                break

        # Final cost after processing
        cycles = self.compute_cost(processed_key_count, complexity)

        # Remove all processed keys from the window
        processed_keys = sum(processed_key_count.values())
        self.keys = self.keys[processed_keys:]

        return processed_keys, cycles, processed_key_count

    def compute_cost(self, processed_key_count: dict[str, int], complexity) -> int:
        """
        Computes the total cycles required for the current processed_key_count.

        Args:
            processed_key_count (dict[str, int]): Dictionary of keys and their occurrences.
            complexity (Complexity): Complexity object to calculate computational cycles.

        Returns:
            int: The total cycles required to process the current keys.
        """
        total_cycles = 0
        for occurrences in processed_key_count.values():
            total_cycles += complexity.calculate_cycles(occurrences)

        return total_cycles

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
