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

        # Calculate the frequency probabilities for each key
        # For simplicity, use a normal distribution centered around the mean
        key_probabilities = np.random.normal(self.mean, self.stddev, len(self.keys))

        # Use exp to ensure all probabilities are positive
        key_probabilities = np.exp(key_probabilities)

        # Normalize to make probabilities sum to 1
        key_probabilities /= np.sum(key_probabilities)

        # Generate the keys based on these probabilities
        num_keys = int(arrival_rate)
        generated_keys = np.random.choice(self.keys, size=num_keys, p=key_probabilities)

        return generated_keys.tolist()
