# complexities.py
from .Complexity import Complexity
import math


class O1Complexity(Complexity):
    def calculate_cycles(self, n: int) -> int:
        return 1


class OLogNComplexity(Complexity):
    def calculate_cycles(self, n: int) -> int:
        return math.ceil(math.log(n + 1, 2))


class ONComplexity(Complexity):
    def calculate_cycles(self, n: int) -> int:
        return n


class ONLogNComplexity(Complexity):
    def calculate_cycles(self, n: int) -> int:
        return math.ceil(n * math.log(n + 1, 2))


class ON2Complexity(Complexity):
    def calculate_cycles(self, n: int) -> int:
        return n * n