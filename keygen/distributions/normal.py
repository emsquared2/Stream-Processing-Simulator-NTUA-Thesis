import random
import numpy as np
from .base import Distribution


class NormalDistribution(Distribution):
    def __init__(self, keys, mean, stddev):
        super().__init__(keys)
        self.mean = mean
        self.stddev = stddev

    def generate(self, arrival_rate):
        count = int(np.random.normal(self.mean, self.stddev))
        count = max(0, min(count, len(self.keys)))  # Ensure count is within valid range
        return random.choices(self.keys, k=count)
