from entity.ecc_point import ECCPoint
from typing import List

class IntPair:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"IntPair({self.x}, {self.y})"

class EccPointPair:
    def __init__(self, x: ECCPoint, y: ECCPoint):
        self.first = x
        self.second = y

    def __eq__(self, other):
        return self.first == other.first and self.second == other.second

    def __hash__(self):
        return hash((self.first, self.second))

    def __repr__(self):
        return f"EccPointPair({self.first}, {self.second})"

class ProofOfWork:
    def __init__(self, A: List[ECCPoint], B: list[ECCPoint], u: list[int], w: list[int]):
        self.A = A
        self.B = B
        self.u = u
        self.w = w

    def __eq__(self, other):
        return (
            self.A == other.A and
            self.B == other.B and
            self.u == other.u and
            self.w == other.w
        )

    def __hash__(self):
        return hash((tuple(self.A), tuple(self.B), tuple(self.u), tuple(self.w)))