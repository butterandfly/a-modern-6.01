import sys
sys.path.insert(1, '../lib')

from sm import StateMachine, Wire, Delay1, Parallel, SimpleFeedback, Cascade, Adder

fibonacci = SimpleFeedback(Cascade(Parallel(Wire(), Delay1(0)), Adder()), 1)
results = fibonacci.run(10, verbose=True)
print('Fibonacci numbers:')
print(results)
