import sys
sys.path.insert(1, './lib')

from sm import Cascade, Multiplier, Feedback2, make_counter, Delay

fact = Cascade(make_counter(1, 1),
               Feedback2(Cascade(Multiplier(), Delay(1))))

fact.run(10, verbose=True)