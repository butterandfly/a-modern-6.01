import math
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class Signal(ABC):
    @abstractmethod
    def sample(self, n: int):
        pass

    def plot(self, start: int = 0, end: int = 100):
        xs = range(start, end)
        ys = [self.sample(i) for i in xs]
        plt.stem(xs, ys)
        plt.show()

    def __mul__(self, scale: float):
        return ScaledSignal(self, scale)

    def __rmul__(self, scale: float):
        return ScaledSignal(self, scale)

    def __add__(self, other):
        return SummedSignal(self, other)

class ScaledSignal(Signal):
    def __init__(self, signal: Signal, scale: float):
        self.signal = signal
        self.scale = scale

    def sample(self, n: int):
        return self.scale * self.signal.sample(n)

class SummedSignal(Signal):
    def __init__(self, s1: Signal, s2: Signal):
        self.s1 = s1
        self.s2 = s2

    def sample(self, n: int):
        return self.s1.sample(n) + self.s2.sample(n)

class R(Signal):
    def __init__(self, s: Signal):
        self.s = s

    def sample(self, n: int):
        return self.s.sample(n - 1)

class Rn(Signal):
    def __init__(self, s: Signal, n: int):
        self.s = s
        self.n = n

    def sample(self, n: int):
        return self.s.sample(n - self.n)

class UnitSampleSignal(Signal):
    def sample(self, n: int):
        return 1 if n == 0 else 0

class ConstantSignal(Signal):
    def __init__(self, c: float):
        self.c = c

    def sample(self, n: int):
        return self.c

class CosineSignal(Signal):
    def __init__(self, omega: float = 1, phase: float = 0):
        self.omega = omega
        self.phase = phase

    def sample(self, n):
        return math.cos(self.omega * n + self.phase)

# unit_sample = UnitSampleSignal()
# unit_sample.plot()

# constant = ConstantSignal(4)
# constant.plot()

# cosine = CosineSignal(0.1, 0)
# cosine.plot()

s = (4 * UnitSampleSignal()) + ConstantSignal(1)
s.plot()
