from Crypto.Util.number import inverse, getRandomRange
from utils.ecc import legendre_symbol, square_root
from entity.ecc_point import ECCPoint

class EllipticCurve:
    def __init__(self, a: int, b: int, p: int):
        self.a = a % p
        self.b = b % p
        self.p = p

        if (4 * self.a ** 3 + 27 * self.b ** 2) % self.p == 0:
            raise ValueError("Invalid curve parameters: 4a^3 + 27b^2 must not be congruent to 0 mod p.")

    def is_on_curve(self, point: ECCPoint) -> bool:
        """Check if a point lies on the curve."""
        if point.is_origin:
            return True
        x, y = point.x, point.y
        return (y ** 2 - x ** 3 - self.a * x - self.b) % self.p == 0

    def negation_point(self, point: ECCPoint) -> ECCPoint:
        """Return the negation of a point."""
        if point.is_origin:
            return ECCPoint(0, 0, True)
        return ECCPoint(point.x, (-point.y) % self.p)

    def add(self, point_1: ECCPoint, point_2: ECCPoint) -> ECCPoint:
        """Add two points on the curve."""
        if not self.is_on_curve(point_1) or not self.is_on_curve(point_2):
            raise ValueError("One or both points are not on the curve.")

        if point_1.is_origin:
            return point_2
        if point_2.is_origin:
            return point_1
        if point_1 == self.negation_point(point_2):
            return ECCPoint(0, 0, True)

        if point_1 != point_2:
            numerator = (point_2.y - point_1.y) % self.p
            denominator = inverse((point_2.x - point_1.x) % self.p, self.p)
        else:
            numerator = (3 * point_1.x ** 2 + self.a) % self.p
            denominator = inverse((2 * point_1.y) % self.p, self.p)

        L = (numerator * denominator) % self.p
        x3 = (L ** 2 - point_1.x - point_2.x) % self.p
        y3 = (L * (point_1.x - x3) - point_1.y) % self.p
        return ECCPoint(x3, y3)

    def sub(self, point_1: ECCPoint, point_2: ECCPoint) -> ECCPoint:
        """Subtract two points on the curve."""
        return self.add(point_1, self.negation_point(point_2))

    def multiply(self, value: int, point: ECCPoint) -> ECCPoint:
        """Multiply a point by a scalar."""
        if not self.is_on_curve(point):
            raise ValueError("The point is not on the curve.")
        if value < 0:
            value = -value
            point = self.negation_point(point)

        result = ECCPoint(0, 0, True)
        temp = point
        while value:
            if value & 1:
                result = self.add(result, temp)
            temp = self.add(temp, temp)
            value >>= 1
        return result

    def gens(self) -> ECCPoint:
        """Generate a random point on the curve."""
        while True:
            x = getRandomRange(1, self.p)
            y_square = (x ** 3 + self.a * x + self.b) % self.p
            if legendre_symbol(y_square, self.p) == 1:
                return ECCPoint(x, square_root(y_square, self.p))

    def __repr__(self) -> str:
        return f"Elliptic Curve over F_{self.p}: y^2 = x^3 + {self.a}x + {self.b}"