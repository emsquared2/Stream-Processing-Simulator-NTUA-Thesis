from abc import ABC, abstractmethod
from typing import List, Any


class PartitionStrategy(ABC):
    """
    Abstract base class for partitioning strategies.

    Methods:
    partition(keys: List[str], nodes: List[Any], buffers: dict) -> None:
        Abstract method to partition keys among nodes.
    """

    @abstractmethod
    def partition(self, keys: List[str], nodes: List[Any], buffers: dict) -> None:
        pass
