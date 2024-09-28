import numpy as np
from .base import Distribution


class ZipfDistribution(Distribution):
    """Zipf distribution class for generating keys."""

    def __init__(self, keys, alpha):
        """Constructor for the ZipfDistribution class.

        Args:
            keys (list): List of keys to be used in the distribution.
            alpha (float): The parameter of the Zipf distribution which controls
                           the skewness of the distribution. Higher values make
                           the distribution more skewed.
        """
        super().__init__(keys)
        self.alpha = alpha

    def generate(self, arrival_rate):
        """Generate keys based on a Zipf distribution.

        Args:
            arrival_rate (int): The number of keys to generate.

        Returns:
            list: A list of keys chosen based on the Zipf distribution.
        """
        num_keys = int(arrival_rate)

        # Generate a Zipf distribution of indices (wrapped to valid indices)
        indices = np.random.zipf(a=self.alpha, size=num_keys)

        # Wrapping indices to fit the length of keys
        wrapped_indices = (indices - 1) % len(self.keys)

        # Return the actual keys based on the generated indices
        return [self.keys[i] for i in wrapped_indices]
