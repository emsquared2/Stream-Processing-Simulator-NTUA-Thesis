from topology.Topology import Topology
from utils.ConfigValidator import validate_topology


class Simulator:
    """
    A class to simulate the distribution and processing of keys across multiple nodes.

    Attributes:
    - topology (Topology): A class representing the simulator topology.
    - input_partitioner (KeyPartitioner): A KeyPartitioner class that will
                                          partition the input keys to the
                                          first stage.
    """

    def __init__(self, topology_config: dict):
        """
        Initializes a new Simulator instance with the given parameters.

        Args:
        - topology (dict): A dictionary representing the entire topology.
        """

        # Validate the topology configuration
        validate_topology(topology_config)

        # Initialize the topology
        self.topology = Topology(topology_config)

        # Select the first node from stage 0 which is the initial partitioner
        self.input_partitioner = self._find_stage0_partitioner()

    def _find_stage0_partitioner(self):
        """
        Selects the first node from the stage with id '0' which is the initial partitioner.

        Returns:
        - Node: Returns the first node of the stage 0. In our case
                its the initial input (key) partitioner.
        """
        for stage in self.topology.stages:
            if stage.id == 0:
                return stage.nodes[0]
        raise ValueError("Stage with id '0' not found in the topology.")

    def sim(self, steps_data):
        """
        Simulates the reception and processing of keys across multiple steps.

        Args:
        - steps_data (list): A list of lists, where each sublist contains keys received in a step.
        """

        for step_count, step_keys in enumerate(steps_data):
            self.input_partitioner.receive_and_process(step_keys, step_count)

        # Print the final state of all nodes
        self.report()

    def report(self):
        """
        Prints the final state of all nodes after the simulation.
        """
        final_state_message = """
------------------------
|                      |
|     Final State      |
|                      |
------------------------
"""
        print(final_state_message)
        print(self.topology)
