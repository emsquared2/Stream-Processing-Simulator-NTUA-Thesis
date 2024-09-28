import numpy as np
from .base import Distribution


class PoissonDistribution(Distribution):
    """Poisson distribution class for generating keys."""

    def __init__(self, keys, lam):
        """Constructor for the PoissonDistribution class.

        Args:
            keys (list): List of keys to be used in the distribution.
            lam (float): The lambda (λ) parameter of the Poisson distribution,
                         which represents the rate at which events occur.
        """
        super().__init__(keys)
        self.lam = lam

    def generate(self, arrival_rate):
        """Generate keys based on a Poisson distribution.

        Args:
            arrival_rate (int): The number of keys to generate.

        Returns:
            list: A list of keys chosen based on the Poisson distribution.
        """
        num_keys = int(arrival_rate)

        # Generate a Poisson distribution of indices (rounded and wrapped to valid indices)
        indices = np.random.poisson(lam=self.lam, size=num_keys)
        wrapped_indices = indices % len(self.keys)

        # Return the actual keys based on the generated indices
        return [self.keys[i] for i in wrapped_indices]
