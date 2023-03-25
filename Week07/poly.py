import numpy as np
# A polynomial class
#class Polynomial:


# A polynomial class using np.poly1d
class Polynomial:
    @classmethod
    def from_poly1d(cls, poly1d):
        return cls(poly1d.coeffs.tolist())

    @classmethod
    def add(cls, p1, p2):
        return cls.from_poly1d(p1.poly1d + p2.poly1d)

    @classmethod
    def mul(cls, p1, p2):
        return cls.from_poly1d(p1.poly1d * p2.poly1d)

    @classmethod
    def shift(cls, p: any, a: int):
        return Polynomial(p.coeffs + ([0] * a))

    coeffs: list

    def __init__(self, coeffs: list):
        self.poly1d = np.poly1d(coeffs)
        self.coeffs = coeffs
        self.order = len(coeffs) - 1

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_string()

    def __add__(self, other):
        return Polynomial.add(self, other)

    def __sub__(self, other):
        return Polynomial.add(self, other.scalar_mul(-1))

    def __mul__(self, other):
        return Polynomial.mul(self, other)

    def __call__(self, x):
        return self.val(x)

    def scalar_mul(self, scalar):
        return Polynomial.from_poly1d(self.poly1d * scalar)

    def val(self, x):
        return self.poly1d(x)

    def roots(self):
        return self.poly1d.r.tolist()

    def to_string(self, var="x"):
        result = ""
        order = self.order
        for i in range(order, -1, -1):
            if i == 0:
                result = f'{result}{self.coeffs[order - i]}'
            elif i == 1:
                result = f'{result}{self.coeffs[order - i]}{var} + '
            else:
                result = f'{result}{self.coeffs[order - i]}{var}**{i} + '
        return result


# p = Polynomial.from_poly1d(np.poly1d([1, 2, 1]))
# print(Polynomial.add(p, p).coeffs)

# p = np.poly1d([1,2,3])
# print(p * p)
# print(p*2)