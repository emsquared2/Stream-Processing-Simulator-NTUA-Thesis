from simulator.GlobalConfig import GlobalConfig
from .Node import Node
from utils.utils import create_complexity
from utils.Logging import initialize_logging, log_default_info, log_node_info


class AggregationNode(Node):
    """
    Represents a node for aggregation tasks in the simulation.

    Inherits from the abstract Node class and sets the uid in the format '1_aggr'.
    """

    def __init__(
        self, stage_node_id: int, complexity_type: str, stage, window_size: int, slide: int, terminal: bool = False
    ) -> None:
        """
        Initializes an AggregationNode with a custom uid and specified parameters.

        Args:
            stage_node_id: The stage local node identifier.
            throughput (int): Maximum computational cycles a node can run per step.
            stage (Stage): The stage which the node is in.
        """
        # Construct the uid in the desired format
        uid = f"{stage_node_id}_aggr"

        # Initialize the base class with the custom uid
        # Note: ATM for the AggregationNode we consider that throughput to be equal to 0.
        super().__init__(uid, stage_node_id, "Aggregation", -1, stage)

        self.state: dict[int, dict[str, int]] = {}
        self.complexity = create_complexity(complexity_type)
        self.window_size = window_size
        self.slide = slide
        self.terminal = terminal
        self.finished: list[bool] = [False] * len(stage.nodes)

        self.extra_dir = GlobalConfig.extra_dir

        # Initialize logging
        self.default_logger, self.node_logger, _ = initialize_logging(
            self.uid, self.extra_dir
        )

    def receive_and_process(
        self, keys: dict[int, list[dict[str, int]]], step: int, sender_stage_node_id
    ) -> None:
        """
        Process the keys for this aggregation node.

        Args:
            keys (dict): Dict of keys to be processed.
            step (int): Current step in the simulation.
            sender_stage_node_id: The sender stage node ID.
        """
        print(keys, step, sender_stage_node_id)

        log_node_info(
            self.node_logger,
            f"Received keys: {keys} at step {step} from node {sender_stage_node_id}",
            self.uid
        )

        if keys:
            for window_step, key_count_list in keys.items():
                # Initialize the state for window_step if it doesn't exist
                if window_step not in self.state:
                    self.state[window_step] = {}

                # Loop through the list of dictionaries and update the count in the dictionary
                for key_count_dict in key_count_list:
                    for key, count in key_count_dict.items():
                        if key == "finished":
                            self.finished[sender_stage_node_id] = True
                            if all(self.finished) or self.is_expired(window_step, step):
                                cycles, emitting_keys = self.process(key_count_list)
                                if not self.terminal:
                                    self.emit_keys(emitting_keys, step)
                        else:
                            # Add the count to the existing key or initialize it if not present
                            if key in self.state[window_step]:
                                self.state[window_step][key] += count
                            else:
                                self.state[window_step][key] = count

    def emit_keys(self, keys: list, step: int) -> None:
        print(keys)
        log_node_info(
            self.node_logger,
            f"Emitting {keys} in step {step}",
            self.uid,
        )
        self.stage.next_stage.nodes[0].receive_and_process(keys, step)

    def is_expired(self, window_step: int, step: int):
        return step > window_step + 3 * self.slide + self.window_size

    def process(self, key_count_list: list[tuple[str, int]]):
        print(key_count_list)
        cycles = 0
        emitting_keys = []

        log_node_info(
            self.node_logger,
            f"Processing {key_count_list}",
            self.uid,
        )

        for key_count_dict in key_count_list:
            for key, count in key_count_dict.items():
                if key != "finished": 
                    cycles += self.complexity.calculate_cycles(count)
                    emitting_keys.append(key)

        return cycles, emitting_keys
