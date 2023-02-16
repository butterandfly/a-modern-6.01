import sm

class TestSM(sm.StateMachine):
    start_state = 0
    def get_next_values(self, state, input):
        if state == 0:
            return (1, True)
        else:
            return (0, True)


def test_start():
    tsm = TestSM()
    tsm.start()
    assert tsm.state == 0

def test_step():
    tsm = TestSM()
    tsm.start()

    output = tsm.step('a')
    assert tsm.state == 1
    assert output == True

def test_transduce():
    tsm = TestSM()
    tsm.start()

    outputs = tsm.transduce(['a', 'b', 'c'])
    assert tsm.state == 1
    assert outputs == [True, True, True]

def test_transduce_verbose():
    tsm = TestSM()
    tsm.start()

    outputs = tsm.transduce(['a', 'b', 'c'], verbose=True)
    assert tsm.state == 1
    assert outputs == [True, True, True]