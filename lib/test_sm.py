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

# Test the SimpleFeeback class
class TestSimpleFeedback:
    def test_init(self):
        plus_one = PlusOne()
        feedback = sm.SimpleFeedback(plus_one, 100)

        assert feedback.machine == plus_one
        assert feedback.start_state == 0
        assert feedback.first_input == 100

    def test_get_next_values(self):
        plus_one = PlusOne()
        feedback = sm.SimpleFeedback(plus_one, 100)

        next_state, output = feedback.get_next_values(0, 10)
        assert next_state == 11
        assert output == 11

        next_state, output = feedback.get_next_values(11, 10)
        assert next_state == 11
        assert output == 11

    def test_run(self):
        plus_one = PlusOne()
        feedback = sm.SimpleFeedback(plus_one, 100)

        outputs = feedback.run(n=3)
        assert outputs == [101, 102, 103]

class TestDelay0:
    def test_get_next_values(self):
        delay = sm.Delay0()
        next_state, output = delay.get_next_values(0, 7)
        assert next_state == 7
        assert output == 7

class TestDelay1:
    def test_init(self):
        delay = sm.Delay1(7)
        assert delay.start_state == 7

    def test_get_next_values(self):
        delay = sm.Delay1(7)
        next_state, output = delay.get_next_values(7, 14)
        assert next_state == 14
        assert output == 7

class TestAdder:
    def test_get_next_values(self):
        adder = sm.Adder()
        _, output = adder.get_next_values(0, (1, 2))
        assert output == 3