from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def calculate_cycles(self, n: int) -> int:
        """
        Calculate the computational cycles required for processing 'n' keys.

        Args:
            n (int): The number of keys being processed.

        Returns:
            int: The computational cycles required.
        """
        pass

    def to_str(self) -> str:
        """
        Returns the operation type as a string.

        Returns:
            str: The operation type string.
        """
        pass
