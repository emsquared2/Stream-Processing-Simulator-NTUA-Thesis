import random
from .base import Distribution


class UniformDistribution(Distribution):
    """Uniform distribution class for generating keys."""

    def generate(self, arrival_rate):
        """Generate keys based on a uniform distribution.

        Args:
            arrival_rate (int): The number of keys to generate.

        Returns:
            list: A list of keys chosen uniformly at random.
        """
        return random.choices(self.keys, k=arrival_rate)
