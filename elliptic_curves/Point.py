from finite_fields.FieldElement import FieldElement

class Point:
    def __init__(self, x, y, a, b) -> None:
        self.a = a
        self.b = b

        self.x = x
        self.y = y

        if self.x is None and self.y is None:
            return

        self._check_elliptic_curve_eq(self.x, self.y, self.a, self.b)
    
    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        elif isinstance(self.x, FieldElement):
            return 'Point({},{})_{}_{} FieldElement({})'.format(
                self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime)
        else:
            return 'Point({},{})_{}_{}'.format(self.x, self.y, self.a, self.b)

    def __eq__(self, other) -> bool:
        return (
            (self.a == other.a) and
            (self.b == other.b) and
            (self.x == other.x) and
            (self.y == other.y)
        )

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(
                "Points {}, {} are not in the same elliptic curve".format(self, other)
            )
        
        if self.x is None:
            return other
        if other.x is None:
            return self
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        if self.x != other.x:  # distinct points
            s = (other.y - self.y) / (other.x - self.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        if self == other and self.y == 0 * self.x: # tangent line is vertical
            return self.__class__(None, None, self.a, self.b)

        if self == other:  # point doubling
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s**2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

    def __rmul__(self, coefficient):
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)

        while coef:
            if coef & 1: # check last bit
                result += current
            current += current # doubles the point
            coef >>= 1 # 1 bit shift of the coefficient
        return result

    def _check_elliptic_curve_eq(self, x, y, a, b):
        if y**2 != x**3 + a*x + b:
            raise ValueError(
                "({}, {}) is not on the curve with parameters ({}, {})".format(x,y,a,b)
            )

