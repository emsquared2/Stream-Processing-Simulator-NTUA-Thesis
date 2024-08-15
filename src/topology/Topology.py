from .stage.Stage import Stage


class Topology:
    def __init__(self, topology_config, extra_dir):
        """
        Initializes the Topology with stages based on the given topology configuration.

        Args:
            topology_config (dict): A dictionary representing the entire topology.
        """
        self.stages = self._create_stages(topology_config["stages"], extra_dir)

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
        stages_repr = "\n".join(f"Stage {stage.id}: {stage}" for stage in self.stages)
        return (
            f"\n######### T O P O L O G Y #########\n"
            f"Total stages: {len(self.stages)}\n"
            f"{stages_repr}\n"
            f"###################################\n"
        )
