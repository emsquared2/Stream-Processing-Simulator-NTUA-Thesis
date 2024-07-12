from abc import ABC, abstractmethod
from typing import List, Any

class PartitionStrategy(ABC):
    @abstractmethod
    def partition(self, keys: List[str], nodes: List[Any]) -> None:
        pass
