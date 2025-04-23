class ECCPoint:
    def __init__(self, x: int, y: int, origin: bool = False):
        self._x = x
        self._y = y
        self._origin = origin

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def is_origin(self) -> bool:
        return self._origin

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ECCPoint):
            return False
        if self.is_origin and other.is_origin:
            return True
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.is_origin))

    def __repr__(self) -> str:
        if self.is_origin:
            return "ECC Point (Origin)"
        return f"ECC Point ({self.x}, {self.y})"