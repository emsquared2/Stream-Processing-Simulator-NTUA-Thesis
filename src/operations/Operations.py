from .Operation import Operation
import math


class StatelessOperation(Operation):
    def calculate_cycles(self, n: int) -> int:
        return 1

    def to_str(self) -> str:
        return "StateLessOperation"


class BinaryOperation(Operation):
    def calculate_cycles(self, n: int) -> int:
        return math.ceil(math.log(n + 1, 2))

    def to_str(self) -> str:
        return "BinaryOperation"


class Aggregation(Operation):
    def calculate_cycles(self, n: int) -> int:
        return n

    def to_str(self) -> str:
        return "Aggregation"


class Sorting(Operation):
    def calculate_cycles(self, n: int) -> int:
        return math.ceil(n * math.log(n + 1, 10))

    def to_str(self) -> str:
        return "Sorting"


class NestedLoop(Operation):
    def calculate_cycles(self, n: int) -> int:
        return n * n

    def to_str(self) -> str:
        return "NestedLoop"
