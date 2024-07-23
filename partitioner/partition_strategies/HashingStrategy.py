
from typing import Any, List
from partition_strategies.PartitionStrategy import PartitionStrategy

class HashingStrategy(PartitionStrategy):
    def partition(self, keys: List[str], nodes: List[Any]) -> None:
        for key in keys:
            node_index = hash(key) % len(nodes)
            nodes[node_index].receive(key)
