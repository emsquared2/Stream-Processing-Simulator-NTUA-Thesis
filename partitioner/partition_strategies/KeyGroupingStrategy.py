from typing import Any, List
from partition_strategies.PartitionStrategy import PartitionStrategy

class KeyGroupingStrategy(PartitionStrategy):
    def __init__(self, prefix_length = 1):
        self.prefix_length = prefix_length
        self.group_map = {}  # Dictionary to map key groups to nodes

    def partition(self, keys: List[str], nodes: List[Any]) -> None:
        for key in keys:
            group_key = key[:self.prefix_length]
            node_index = hash(group_key) % len(nodes)
            nodes[node_index].receive(key)
            if group_key not in self.group_map:
                self.group_map[group_key] = node_index

    def get_node_index(self, key: str) -> int:
        group_key = key[:self.prefix_length]
        return self.group_map.get(group_key, -1)
