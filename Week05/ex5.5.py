import sys
sys.path.insert(1, './lib')

import sm

m1 = sm.ParallelAdd(sm.Wire(), sm.Cascade(sm.Gain(-1), sm.R(2)))
m2 = sm.R(3)

m3 = sm.Cascade(m1, m2)
m3.transduce(range(10), verbose=True)

m4 = sm.Cascade(m2, m1)
m4.transduce(range(10), verbose=True)