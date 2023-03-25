from poly import Polynomial
import numpy as np

class SystemFunction:
    numerator: Polynomial
    denominator: Polynomial

    def __init__(self, num: Polynomial, den: Polynomial):
        self.numerator = num
        self.denominator = den

    def __str__(self) -> str:
        return f"{self.numerator.to_string('R')} / {self.denominator.to_string('R')}"

    def poles(self):
        p = Polynomial(self.denominator.coeffs[::-1])
        return p.roots()

    def poles_magnitude(self):
        return [abs(p) for p in np.real(self.poles())]

    def dominant_pole(self):
        return max(self.poles_magnitude())

    def difference_equation(self):
        # Reverse the list
        c_coeffs = self.denominator.coeffs[::-1]
        # Change the sign
        c_coeffs = [c * -1 for c in c_coeffs]
        # Remove the first element
        c_coeffs.pop(0)

        return DifferenceEquation(self.numerator.coeffs[::-1], c_coeffs)

class DifferenceEquation:
    def __init__(self, d_coeffs: list, c_coeffs: list):
        self.d_coeffs = d_coeffs
        self.c_coeffs = c_coeffs

    def __str__(self) -> str:
        result = "y[n] = "
        for i in range(len(self.c_coeffs)):
            result += f"{self.c_coeffs[i]}y[n-{i+1}] + "
        for j in range(len(self.d_coeffs)):
            if j == 0:
                result += f"{self.d_coeffs[j]}x[n] + "
            else:
                result += f"{self.d_coeffs[i]}x[n-{j}] + "

        return result[:-3]

    def system_function(self):
        num = Polynomial(self.d_coeffs)

        # Reverse the list
        coeffs = self.c_coeffs[::-1]
        # Change the sign
        coeffs = [c * -1 for c in coeffs]
        coeffs.append(1)
        den = Polynomial(coeffs)

        return SystemFunction(num, den)

def cascade(sf1: SystemFunction, sf2: SystemFunction) -> SystemFunction:
    num = sf1.numerator* sf2.numerator
    den = sf1.denominator * sf2.denominator

    return SystemFunction(num, den)

def feedback_subtract(sf1: SystemFunction, sf2: SystemFunction) -> SystemFunction:
    num = sf1.numerator * sf2.denominator
    den = sf1.denominator * sf2.denominator + sf1.numerator * sf2.numerator

    return SystemFunction(num, den)

sf = SystemFunction(Polynomial([1]), Polynomial([0.63, -1.6, 1]))
print(sf)
print(sf.poles())