from Node import Node
from partition_strategies.HashingStrategy import HashingStrategy
from partition_strategies.KeyGroupingStrategy import KeyGroupingStrategy
from partition_strategies.RoundRobinStrategy import RoundRobinStrategy

class Simulator:
    def __init__(self, num_nodes, strategy_name, prefix_length = 1):
        self.num_nodes = num_nodes
        self.prefix_length = prefix_length
        
        # Create the nodes
        self.nodes = [Node(i) for i in range(num_nodes)]
        
        # Initialize the strategy
        self.strategy = self._init_strategy(strategy_name)
    
    def _init_strategy(self, strategy_name):
        if strategy_name == "round_robin":
            return RoundRobinStrategy()
        elif strategy_name == "hashing":
            return HashingStrategy()
        elif strategy_name == "key_grouping":
            return KeyGroupingStrategy(self.prefix_length)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")


    def sim(self, steps_data):
        
        # Partition the keys
        for step in steps_data:
            self.strategy.partition(step, self.nodes)    

        self.report()
        
    def report(self):
            print("\nFinal state of nodes:")
            for node in self.nodes:
                print(node)
