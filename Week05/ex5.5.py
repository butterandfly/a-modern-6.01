import sys
sys.path.insert(1, './lib')

import sm

def delta_signals(n: int=10):
    return [1] + [0] * (n-1)


def print_outputs(d1, d2, inputs):
    m1 = sm.ParallelAdd(sm.Wire(), sm.Cascade(sm.Gain(-1), sm.R(d1)))
    m2 = sm.R(d2)

    print(f'ParallelAdd:d1={d1} --> R:d2={d2}')
    m3 = sm.Cascade(m1, m2)
    m3.transduce(inputs, verbose=True)

    print(f'R:d2={d2} --> ParallelAdd:d1={d1}')
    m4 = sm.Cascade(m2, m1)
    m4.transduce(inputs, verbose=True)

print_outputs(0, 0, delta_signals(10))

print_outputs(2, 3, delta_signals(10))
