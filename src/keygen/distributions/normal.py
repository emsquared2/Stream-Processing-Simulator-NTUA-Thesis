import numpy as np
from .base import Distribution


class NormalDistribution(Distribution):
    """Normal distribution class for generating keys."""

    def __init__(self, keys, mean, stddev):
        """Constructor for the NormalDistribution class.

        Args:
            keys (list): List of keys to be used in the distribution.
            mean (float): The mean of the normal distribution.
            stddev (float): The standard deviation of the normal distribution.
        """
        super().__init__(keys)
        self.mean = mean
        self.stddev = stddev

    def generate(self, arrival_rate):
        """Generate keys base on a normal distribution.

        Args:
            arrival_rate (int): The number of keys to generate.

        Returns:
            list: A list of keys chosen uniformly at random.
        """
        num_keys = int(arrival_rate)

        # Generate a normal distribution of indices (rounded and wrapped to valid indices)
        indices = np.random.normal(loc=self.mean, scale=self.stddev, size=num_keys).round().astype(int)
        wrapped_indices = indices % len(self.keys)       

        return wrapped_indices
