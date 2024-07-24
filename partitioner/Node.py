class Node:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.received_keys = []
    
    def receive(self, key: str) -> None:
        self.received_keys.append(key)
        print(f"Node {self.node_id} received key: {key}")
    
    def process_key(self, key: str) -> None:
        # TODO
        print(f"Node {self.node_id} processing key: {key}")
    
    def __repr__(self):
        sorted_keys = sorted(self.received_keys)
        return f"Node {self.node_id} with keys: {sorted_keys}"
