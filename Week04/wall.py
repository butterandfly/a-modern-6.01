import sys
sys.path.insert(1, './lib')

from sm import Feedback, Cascade, StateMachine

def safe_mult(a, b):
    if a == 'undefined' or b == 'undefined':
        return 'undefined'
    else:
        return a * b

def safe_add(a, b):
    if a == 'undefined' or b == 'undefined':
        return 'undefined'
    else:
        return a + b

k = -1.5
d_desired = 1.0
delta_t = 0.1
d_start = 5

class WallController(StateMachine):
    def get_next_values(self, state, input):
        velocity = safe_mult(k, safe_add(d_desired, safe_mult(-1, input)))
        return (velocity, velocity)

class WallWorld(StateMachine):
    start_state = d_start
    def get_next_values(self, state, input):
        # new_distance = state - delta_t * input
        new_distance = safe_add(state, safe_mult(-1, safe_mult(delta_t, input)))
        return (new_distance, state)

wall = Feedback(Cascade(WallController(), WallWorld()))
outputs = wall.run(30, verbose=True)
print()
print(outputs)