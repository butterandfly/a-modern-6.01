import sys
sys.path.insert(1, './lib')

from sm import Cascade, Increment, Delay, StateMachine
# from sm import Feedback, Cascade, Increment, Delay, StateMachine

class Feedback(StateMachine):
    def __init__(self, sm):
        super().__init__()
        self.sm = sm
        self.start_state = sm.start_state

    def get_next_values(self, state, input):
        _, output = self.sm.get_next_values(state, 'undefined')
        new_state, _ = self.sm.get_next_values(state, output)
        return (new_state, new_state[1])

def make_counter(start_number, step=1):
    return Feedback(Cascade(Increment(step), Delay(start_number)))

counter = make_counter(0, 1)
counter.run(10, verbose=True)