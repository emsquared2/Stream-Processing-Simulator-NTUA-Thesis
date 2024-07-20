import random
from .base import Distribution


class UniformDistribution(Distribution):
    def generate(self, arrival_rate):
        return random.choices(self.keys, k=arrival_rate)
