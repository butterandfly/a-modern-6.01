import numpy as np
from poly import Polynomial

class TestPolynomial:
    def test_init(self):
        p = Polynomial([1,2,3])
        assert p.coeffs == [1,2,3]
        assert p.order == 2
        assert p.poly1d == np.poly1d([1,2,3])

    def test_from_poly1d(self):
        p1 = Polynomial([1,2,3])
        p2 = Polynomial.from_poly1d(p1.poly1d)
        assert p2.coeffs == [1,2,3]
        assert p2.order == 2
        assert p2.poly1d == np.poly1d([1,2,3])

    def test_add(self):
        p1 = Polynomial([1,2,3])
        p2 = Polynomial([1,2,3])
        p3 = Polynomial.add(p1, p2)
        assert p3.coeffs == [2,4,6]
        # a.all(p3.coeffs == [2,4,6])
        assert p3.order == 2
        assert p3.poly1d == np.poly1d([2,4,6])

    def test_mul(self):
        p1 = Polynomial([1,2,3])
        p2 = Polynomial([1,2,3])
        p3 = Polynomial.mul(p1, p2)
        assert p3.coeffs == [1,4,10,12,9]
        assert p3.order == 4
        assert p3.poly1d == np.poly1d([1,4,10,12,9])

    def test_shift(self):
        p1 = Polynomial([1,2,3])
        p2 = Polynomial.shift(p1, 2)
        assert p2.coeffs == [1,2,3,0,0]
        assert p2.order == 4
        assert p2.poly1d == np.poly1d([1,2,3,0,0])

    def test_scalar_mul(self):
        p1 = Polynomial([1,2,3])
        p2 = p1.scalar_mul(2)
        assert p2.coeffs == [2,4,6]
        assert p2.order == 2
        assert p2.poly1d == np.poly1d([2,4,6])

    def test_val(self):
        p1 = Polynomial([1,2,3])
        assert p1.val(1) == 6
        assert p1.val(2) == 11

    def test_roots(self):
        p1 = Polynomial([1,2,1])
        assert p1.roots() == np.poly1d([1,2,1]).r.tolist()

    def test_to_string(self):
        p1 = Polynomial([3,2,1])
        assert p1.to_string() == "3x**2 + 2x + 1"
        assert p1.to_string("y") == "3y**2 + 2y + 1"

        p1 = Polynomial([1,0])
        assert p1.to_string() == "1x + 0"