from typing import Any, List
from partition_strategies.PartitionStrategy import PartitionStrategy

class RoundRobinStrategy(PartitionStrategy):
    def __init__(self):
        self.current_index = 0
    
    def partition(self, keys: List[str], nodes: List[Any]) -> None:
        for key in keys:
            nodes[self.current_index].receive(key)
            self.current_index = (self.current_index + 1) % len(nodes)
