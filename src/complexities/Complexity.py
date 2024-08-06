# complexities.py

from abc import ABC, abstractmethod


class Complexity(ABC):
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