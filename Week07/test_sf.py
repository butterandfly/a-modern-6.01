import sf
from sf import SystemFunction, DifferenceEquation
from poly import Polynomial

class TestSystemFunction:
    def test_poles(self):
        sf = SystemFunction(Polynomial([1]), Polynomial([0.63, -1.6, 1]))
        roots = Polynomial([1, -1.6, 0.63]).roots()
        assert sf.poles() == roots

    def test_poles_magnitude(self):
        sf = SystemFunction(Polynomial([1]), Polynomial([0.63, -1.6, 1]))
        roots = Polynomial([1, -1.6, 0.63]).roots()
        assert sf.poles_magnitude() == [abs(r) for r in roots]

    def test_dominant_pole(self):
        sf = SystemFunction(Polynomial([1]), Polynomial([0.63, -1.6, 1]))
        roots = Polynomial([1, -1.6, 0.63]).roots()
        assert sf.dominant_pole() == max([abs(r) for r in roots])

    def test_difference_equation(self):
        sf = SystemFunction(Polynomial([1, 2]), Polynomial([0.63, -1.6, 1]))
        de = sf.difference_equation()
        assert de.c_coeffs == [1.6, -0.63]
        assert de.d_coeffs == [2, 1]

    def test_str(self):
        sf = SystemFunction(Polynomial([1]), Polynomial([0.63, -1.6, 1]))
        assert str(sf) == "1 / 0.63R**2 + -1.6R + 1"

class TestDifferenceEquation:
    def test_str(self):
        de = DifferenceEquation([1], [1.6, -0.63])
        assert str(de) == "y[n] = 1.6y[n-1] + -0.63y[n-2] + 1x[n]"

    def test_system_function(self):
        de = DifferenceEquation([1], [1.6, -0.63])
        sf = de.system_function()
        roots = Polynomial([1, -1.6, 0.63]).roots()
        assert sf.poles() == roots

def test_cascade():
    sf1 = SystemFunction(Polynomial([-2, 1]), Polynomial([-1, 1]))
    sf2 = SystemFunction(Polynomial([1, 0, 1]), Polynomial([-1, 1]))
    sf3 = sf.cascade(sf1, sf2)
    assert sf3.numerator.coeffs == [-2, 1, -2, 1]
    assert sf3.denominator.coeffs == [1, -2, 1]

def test_feedback_subtract():
    sf1 = SystemFunction(Polynomial([1]), Polynomial([1, 1]))
    sf2 = SystemFunction(Polynomial([1]), Polynomial([-1, 1]))
    sf3 = sf.feedback_subtract(sf1, sf2)
    assert sf3.numerator.coeffs == [-1, 1]
    assert sf3.denominator.coeffs == [-1, 0, 2]