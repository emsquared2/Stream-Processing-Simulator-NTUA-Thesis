from node.StatelessNode import StatelessNode
from node.StatefulNode import StatefulNode


class Stage:
    def __init__(self, stage_data, extra_dir):
        """
        Initializes the Stage with nodes based on the given stage data.

        Args:
            stage_data (dict): A dictionary representing a stage in the topology.
        """
        self.id = stage_data["id"]
        self.nodes = self._create_nodes(stage_data["nodes"], extra_dir)

    def _create_nodes(self, nodes_data, extra_dir):
        """
        Creates instances of nodes based on their type.

        Args:
            nodes_data (list): List of dictionaries representing node configurations.

        Returns:
            list: A list of Node instances (StatefulNode or StatelessNode).
        """
        nodes = []
        for node_data in enumerate(nodes_data):
            node_id = node_data["id"]
            node_type = node_data["type"]
            throughput = node_data["throughput"]
            complexity_type = node_data["complexity_type"]
            if node_type == "stateful":
                window_size = node_data["window_size"]
                slide = node_data["slide"]
                node = StatefulNode(
                    node_id, throughput, complexity_type, window_size, slide, extra_dir
                )
            elif node_type == "stateless":
                node = StatelessNode(node_id, throughput, complexity_type, extra_dir)
            nodes.append(node)
        return nodes

    def __repr__(self):
        return f"Stage {self.id} with {len(self.nodes)} nodes."
