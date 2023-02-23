from lib.sm import StateMachine

class ABCAcceptor(StateMachine):
    start_state = 0
    def get_next_values(self, state, inp):
        if state == 0 and inp == 'a':
            return (1, True)
        elif state == 1 and inp == 'b':
            return (2, True)
        elif state == 2 and inp == 'c':
            return (0, True)
        else:
            return (3, False)
  
def ABCAcceptor_example():
    abc_acceptor = ABCAcceptor()
    abc_acceptor.transduce(['a', 'b', 'c'], verbose=True)
    abc_acceptor.transduce(['a', 'a', 'a'], verbose=True)

class UpDown(StateMachine):
    start_state = 0
    def get_next_values(self, state, inp):
        if inp == 'u':
            new_state = state + 1
            return (new_state, new_state)
        else:
            new_state = state - 1
            return (new_state, new_state)

def UpDown_example():
    up_down = UpDown()
    up_down.transduce(['u', 'u', 'd'], verbose=True)
 
class Delay(StateMachine):
    def __init__(self, start_state):
        self.start_state = start_state

    def get_next_values(self, state, inp):
        return (inp, state)

def Delay_example():
    delay = Delay(0)
    delay.transduce([1, 2, 3], verbose=True)

class Average2(StateMachine):
    start_state = 0
    def get_next_values(self, state, inp):
        return (inp, (state + inp) / 2)

def Average2_example():
    average2 = Average2()
    average2.transduce([1, 2, 3], verbose=True)

class SumLast3(StateMachine):
    start_state = (0, 0)
    def get_next_values(self, state, inp):
        return ((state[1], inp), state[0] + state[1] + inp)

def SumLast3_example():
    sum_last3 = SumLast3()
    sum_last3.transduce([1, 2, 3, 4, 5, 6], verbose=True)

class SimpleParkingGate(StateMachine):
    start_state = 'waiting'

    def generate_output(self, state):
        if state == 'raising':
            return 'raise'
        elif state == 'lowering':
            return 'lower'
        else:
            return 'nop'

    def get_next_values(self, state, inp):
        gate_position, car_at_gate, car_just_exited = inp
        next_state = None

        if state == 'waiting' and car_at_gate:
            next_state = 'raising'
        elif state == 'raising' and gate_position == 'top':
            next_state = 'raised'
        elif state == 'raised' and car_just_exited:
            next_state = 'lowering'
        elif state == 'lowering' and gate_position == 'bottom':
            next_state = 'waiting'
        else:
            next_state = state

        return (next_state, self.generate_output(next_state))

def safe_add(x, y):
    if x == 'undefined' or y == 'undefined':
        return 'undefined'
    else:
        return x + y

class Increment(StateMachine):
    def __init__(self, incr) -> None:
        super().__init__()
        self.incr = incr

    def get_next_values(self, state, inp):
        output = safe_add(inp, self.incr)
        return (output, output)

ABCAcceptor_example()
UpDown_example()
Delay_example()
Average2_example()
SumLast3_example()