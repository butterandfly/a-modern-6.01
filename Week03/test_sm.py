import sm

class SimpleSM(sm.StateMachine):
    start_state = 0
    def get_next_values(self, state, input):
        if state == 0:
            return (1, True)
        else:
            return (0, True)

class PlusOne(sm.StateMachine):
    start_state = 0
    def get_next_values(self, state, input):
        return (input + 1, input + 1)

class TestStateMachine:
    def test_start(self):
        tsm = SimpleSM()
        tsm.start()
        assert tsm.state == 0

    def test_step(self):
        tsm = SimpleSM()
        tsm.start()

        output = tsm.step('a')
        assert tsm.state == 1
        assert output == True

    def test_transduce(self):
        tsm = SimpleSM()
        tsm.start()

        outputs = tsm.transduce(['a', 'b', 'c'])
        assert tsm.state == 1
        assert outputs == [True, True, True]

    def test_transduce_verbose(self):
        tsm = SimpleSM()
        tsm.start()

        outputs = tsm.transduce(['a', 'b', 'c'], verbose=True)
        assert tsm.state == 1
        assert outputs == [True, True, True]

class TestParallel:
    def test_init(self):
        sm1 = SimpleSM()
        sm2 = SimpleSM()
        
        psm = sm.Parallel(sm1, sm2)

        assert len(psm.machines) == 2
        assert psm.machines[0] == sm1
        assert psm.machines[1] == sm2
        assert psm.start_state == (0, 0)

    def test_get_next_values(self):
        sm1 = SimpleSM()
        sm2 = SimpleSM()
        
        psm = sm.Parallel(sm1, sm2)

        next_state, output = psm.get_next_values((0, 0), ('a', 'b'))
        assert next_state == (1, 1)
        assert output == (True, True)

class TestCascade:
    def test_init(self):
        sm1 = SimpleSM()
        sm2 = SimpleSM()
        
        csm = sm.Cascade(sm1, sm2)

        assert len(csm.machines) == 2
        assert csm.machines[0] == sm1
        assert csm.machines[1] == sm2
        assert csm.start_state == (0, 0)

    def test_get_next_values(self):
        sm1 = PlusOne()
        sm2 = PlusOne()
        
        csm = sm.Cascade(sm1, sm2)

        next_state, output = csm.get_next_values((0, 0), 17)
        assert next_state == (18, 19)
        assert output == 19