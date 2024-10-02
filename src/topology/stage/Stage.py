from typing import Dict, Tuple
from ..node.StatelessNode import StatelessNode
from ..node.KeyPartitioner import KeyPartitioner
from ..node.WorkerNode import WorkerNode
from ..node.AggregatorNode import AggregatorNode

import random


class Stage:
    """
    A simulation topology stage that consists a number of identical nodes.

    Attributes:
    - id (int): Unique stage identifier.
    - stage_type (str): String that describes the type of the stage.
                        It is equivalent to the node type.
    - key_splitting (bool): A flag that determines whether key splitting is applied.
    - next_stage (Stage): Object that specifies the next topology stage.
    - next_stage_len (int): The length of the next stage.
    - terminal_stage (bool): Specifies if the current stage is the last
                             stage of the simulation.
    - hash_seed (int): Seed used in case of hashing partitioning to
                       sync the nodes of the stages.

    - key_node_map (Dict[str, int]): Dictionary used in Power of Two Choices (PoTC) to store the
                                     assigned node for each key. For each key, it stores a single node index,
                                     ensuring consistent routing for the same key across multiple partitioning steps.

    - key_candidates (Dict[str, Tuple[int, int]]): Dictionary used in Partial Key Grouping (PKG)
                                                      to map each key to two candidate nodes. For each key,
                                                      it stores a tuple of two node indices, allowing dynamic
                                                      selection of the least loaded node during partitioning.

    - nodes (list): The nodes of this stage.
    - aggregator (AggregatorNode): The aggregator of the stage. This is used only when key_splitting is applied.
    """

    def __init__(self, stage_data, next_stage_len: int):
        """
        Initializes the Stage with nodes based on the given stage data.

        Args:
            stage_data (dict): A dictionary representing a stage in the topology.
            next_stage_len (int): The number of nodes in the next stage.
        """
        self.id = stage_data["id"]
        self.stage_type = stage_data["type"]
        self.key_splitting = stage_data.get("key_splitting", None)
        self.next_stage = None

        self.next_stage_len = next_stage_len
        self.terminal_stage = next_stage_len == 0

        # Attributes used in partitioning strategies

        self.hash_seed = None
        # PoTC: Tracks the node to which each key is assigned
        self.key_node_map: Dict[str, int] = {}
        # PKG: Tracks two candidate nodes for each key
        self.key_candidates: Dict[str, Tuple[int, int]] = {}

        self.nodes = self._create_nodes(stage_data["nodes"])

        # Initialize Aggregator
        if self.key_splitting:
            self.aggregator = AggregatorNode(
                self.id,
                "Aggregation",
                self,
                stage_data["nodes"][0]["window_size"],
                stage_data["nodes"][0]["slide"],
                stage_data["nodes"][0]["operation_type"],
            )

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
            list: A list of Node instances (WorkerNode or StatelessNode).
        """
        nodes = []

        for i, node_data in enumerate(nodes_data):
            uid = node_data["id"]

            # Here node_type should always be equal to stage_type
            node_type = node_data["type"]

            # TODO: Use of throughput / operation_type on stateless nodes
            throughput = node_data["throughput"]

            if node_type == "stateful":
                operation_type = node_data["operation_type"]
                window_size = node_data["window_size"]
                slide = node_data["slide"]
                node = WorkerNode(
                    uid,
                    i,
                    throughput,
                    operation_type,
                    self,
                    window_size,
                    slide,
                    self.terminal_stage,
                    self.key_splitting,
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
        if self.key_splitting:
            stage_repr += f"\n {self.aggregator}"
        return (
            f"\n---------- Stage {self.id} ----------\n"
            f"Total nodes: {len(self.nodes)}\n"
            f"Key Splitting: {self.key_splitting}\n"
            f"{stage_repr}\n"
            f"----- END  OF  STAGE {self.id} ------\n"
        )
