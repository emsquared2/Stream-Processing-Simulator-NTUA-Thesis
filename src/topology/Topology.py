from .stage.Stage import Stage


class Topology:
    def __init__(self, topology_data, extra_dir):
        """
        Initializes the Topology with stages based on the given topology data.

        Args:
            topology_data (dict): A dictionary representing the entire topology.
        """
        self.stages = self._create_stages(topology_data["stages"], extra_dir)

    def _create_stages(self, stages_data, extra_dir):
        """
        Creates instances of Stage based on the stages data.

        Args:
            stages_data (list): List of dictionaries representing stage configurations.

        Returns:
            list: A list of Stage instances.
        """
        stages = []
        for stage_data in stages_data:
            stage = Stage(stage_data, extra_dir)
            stages.append(stage)
        return stages

    def __repr__(self):
        return f"Topology with {len(self.stages)} stages."
