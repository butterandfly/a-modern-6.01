import sys
sys.path.insert(1, './lib')

from sm import Delay, Parallel, Feedback, Cascade, Adder

fibonacci = Feedback(
    Cascade(
        Parallel(Delay(1), Cascade(Delay(1), Delay(0))), 
        Adder()))
results = fibonacci.run(10, verbose=True)

print()
print('Fibonacci numbers:')
print(results)
