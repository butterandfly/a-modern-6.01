import sm

class TestSM(sm.StateMachine):
    start_state = 0
    def get_next_values(self, state, input):
        return (0, True)


def test_start():
    tsm = TestSM()
    tsm.start()
    assert tsm.state == 0
    #    f"the state after start() is 0 expected, got: {state0}"

def test_step():
    tsm = TestSM()
    tsm.start()

    output = tsm.step('a')
    assert tsm.state == 0
        #f"the state after step('a') is 0 expected, got: {tsm.state}"
    assert output == True
        # f"the output of step('a') is True expected, got: {output}"