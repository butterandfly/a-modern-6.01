from sm import StateMachine

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
 

ABCAcceptor_example()
UpDown_example()