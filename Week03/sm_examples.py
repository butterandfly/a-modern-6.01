from sm import StateMachine

class ABCAcceptor(StateMachine):
    startState = 0
    def get_next_values(self, state, inp):
        if state == 0 and inp == 'a':
            return (1, True)
        elif state == 1 and inp == 'b':
            return (2, True)
        elif state == 2 and inp == 'c':
            return (0, True)
        else:
            return (3, False)

def show_examples():
    abc_acceptor = ABCAcceptor()
    abc_acceptor.start()
    for output in abc_acceptor.trnasduce(['a', 'b', 'c']):
        print(output)

show_examples()