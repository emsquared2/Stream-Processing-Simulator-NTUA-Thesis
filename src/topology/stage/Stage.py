from ..node.StatelessNode import StatelessNode
from ..node.KeyPartitioner import KeyPartitioner
from ..node.StatefulNode import StatefulNode

import random


class Stage:
    def __init__(self, stage_data, next_stage_len: int):
        """
        Initializes the Stage with nodes based on the given stage data.

        Args:
            stage_data (dict): A dictionary representing a stage in the topology.
            next_stage_len (int): The number of nodes in the next stage.
        """
        self.id = stage_data["id"]
        self.stage_type = stage_data["type"]
        self.next_stage = None

        self.next_stage_len = next_stage_len
        self.terminal_stage = next_stage_len == 0

        self.hash_seed = None

        self.nodes = self._create_nodes(stage_data["nodes"])

    def _set_next_stage(self, stage):
        """
        Sets the next stage in the topology.

        Args:
            stage (Stage): The next stage object.
        """
        self.next_stage = stage

    def _create_nodes(self, nodes_data):
        """
        Creates instances of nodes based on their type.

        Args:
            nodes_data (list): List of dictionaries representing node configurations.

        Returns:
            list: A list of Node instances (StatefulNode or StatelessNode).
        """
        nodes = []

        for i, node_data in enumerate(nodes_data):
            uid = node_data["id"]

            # Here node_type should always be equal to stage_type
            node_type = node_data["type"]

            # Question: Use of throughput / complexity_type on
            #           stateless nodes
            throughput = node_data["throughput"]

            if node_type == "stateful":
                complexity_type = node_data["complexity_type"]
                window_size = node_data["window_size"]
                slide = node_data["slide"]
                node = StatefulNode(
                    uid,
                    i,
                    throughput,
                    complexity_type,
                    self,
                    window_size,
                    slide,
                    self.terminal_stage,
                )

            elif node_type == "stateless":
                node = StatelessNode(uid, i, throughput, self)

            # Atm key_partitioner is a StatelessNode but we made
            # it an inherited class so we might have multiple
            # StatelessNode implementations. Also a further bonus
            # is that we clearly state the key paritioning use.
            elif node_type == "key_partitioner":
                strategy_name = node_data["strategy"]["name"]

                strategy_params = {
                    **{key: value for key, value in node_data["strategy"].items()}
                }

                # Add a hash seed on all stage hashing partitioners
                # to ensure same hashing behavior across each stage
                if strategy_name == "hashing":
                    if self.hash_seed is None:
                        self.hash_seed = random.randint(0, 100000)
                    strategy_params["hash_seed"] = self.hash_seed

                node = KeyPartitioner(
                    uid,
                    i,
                    throughput,
                    self,
                    strategy_name,
                    strategy_params,
                )

            nodes.append(node)

        return nodes

    def __repr__(self):
        stage_repr = "\n".join(f"{node}\n" for node in self.nodes)
        return (
            f"\n---------- Stage {self.id} ----------\n"
            f"Total nodes: {len(self.nodes)}\n"
            f"{stage_repr}\n"
            f"----- END  OF  STAGE {self.id} ------\n"
        )
