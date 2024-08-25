from .stage.Stage import Stage


class Topology:
    def __init__(self, topology_config):
        """
        Initializes the Topology with stages based on the given topology configuration.

        Args:
            topology_config (dict): A dictionary representing the entire topology.
        """
        self.stages = self._create_stages(topology_config["stages"])

    def _create_stages(self, stages_data):
        """
        Creates instances of Stage based on the stages data.

        Args:
            stages_data (list): List of dictionaries representing stage configurations.

        Returns:
            list: A list of Stage instances.
        """
        stages = []
        for index, stage_data in enumerate(stages_data):
            if index + 1 < len(stages_data):
                next_stage_len = len(stages_data[index + 1]["nodes"])
            else:
                next_stage_len = 0

            stage = Stage(stage_data, next_stage_len)
            stages.append(stage)

            # # Add stateless intermediate stage (that simulates
            # # the key distribution between stages)
            # if stage.stage_type == "stateful" and next_stage_len != 0:
            #     intermediate_stage = self._create_intermediate_stage(stage.id, len(stage.nodes))
            #     stages.append(intermediate_stage)
            # Now, set the next_stage reference for each Stage instance

        # Reference next_stage in each stage.
        for index in range(len(stages) - 1):
            stages[index]._set_next_stage(stages[index + 1])

        return stages

    def __repr__(self):
        stages_repr = "\n".join(f"{stage}\n\n" for stage in self.stages)
        return (
            f"\n\n######### T O P O L O G Y #########\n\n"
            f"Total stages: {len(self.stages)}\n"
            f"{stages_repr}\n"
            f"#####  END  OF  TOPOLOGY  #####\n\n"
        )
