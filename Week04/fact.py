import sys
sys.path.insert(1, '../lib')

from sm import SimpleFeedback, Cascade, Multiplier, SimpleFeedback2, Increment

fact = Cascade(SimpleFeedback(Increment(), 1), 
               SimpleFeedback2(Multiplier(), 1))

fact.run(10, verbose=True)