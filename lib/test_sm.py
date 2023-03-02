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

class MinusOne(sm.StateMachine):
    start_state = 0
    def get_next_values(self, state, input):
        return (input - 1, input - 1)

class Add(sm.StateMachine):
    start_state = 0
    def get_next_values(self, state, input):
        return (input[0] + input[1], input[0] + input[1])

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

        assert csm.sm1 == sm1
        assert csm.sm2 == sm2
        assert csm.start_state == (0, 0)

    def test_get_next_values(self):
        sm1 = PlusOne()
        sm2 = PlusOne()
        
        csm = sm.Cascade(sm1, sm2)

        next_state, output = csm.get_next_values((0, 0), 17)
        assert next_state == (18, 19)
        assert output == 19

    # def test_run(self):
    #     sm1 = sm.SimpleFeedback(PlusOne(), 0)
    #     sm2 = PlusOne()
        
    #     csm = sm.Cascade(sm1, sm2)

    #     outputs = csm.run(3)
    #     assert outputs == [2, 3, 4]

class TestFeedback:
    def make_counter(self):
        inc = sm.Increment()
        delay = sm.Delay(0)
        cas = sm.Cascade(inc, delay)
        feedback = sm.Feedback(cas)
        return feedback

    def test_init(self):
        feedback = self.make_counter()

        assert feedback.sm.__class__.__name__ == 'Cascade'
        assert feedback.start_state == (0, 0)

    def test_get_next_values(self):
        feedback = self.make_counter()

        next_state, output = feedback.get_next_values((0, 0), None)
        assert next_state == (1, 1)
        assert output == 0

    def test_run(self):
        feedback = self.make_counter()

        outputs = feedback.run(n=3)
        assert outputs == [0, 1, 2]

class TestWire:
    def test_get_next_values(self):
        delay = sm.Wire()
        next_state, output = delay.get_next_values(0, 7)
        assert next_state == 7
        assert output == 7

class TestDelay:
    def test_init(self):
        delay = sm.Delay(7)
        assert delay.start_state == 7

    def test_get_next_values(self):
        delay = sm.Delay(7)
        next_state, output = delay.get_next_values(7, 14)
        assert next_state == 14
        assert output == 7

class TestFeedback2:
    def makeAccumulate(self):
        adder = sm.Adder()
        delay = sm.Delay(0)
        cas = sm.Cascade(adder, delay)
        feedback = sm.Feedback2(cas)
        return feedback

    def test_init(self):
        feedback = self.makeAccumulate()

        assert feedback.sm.__class__.__name__ == 'Cascade'
        assert feedback.start_state == (0, 0)

    def test_get_next_values(self):
        feedback = self.makeAccumulate()

        assert feedback.get_next_values((0, 0), 1) == ((1, 1), 0)

    def test_transduce(self):
        feedback = self.makeAccumulate()

        assert feedback.transduce([1, 2, 3, 4]) == [0, 1, 3, 6]

class TestFeedbackAdd:
    def test_get_next_values(self):
        feedback = sm.FeedbackAdd(sm.Delay(0), sm.Wire())
        assert feedback.transduce([0, 1, 2, 3, 4]) == [0, 0, 1, 3, 6]

class TestAdder:
    def test_get_next_values(self):
        adder = sm.Adder()
        _, output = adder.get_next_values(0, (1, 2))
        assert output == 3

        _, output = adder.get_next_values(0, (1, 'undefined'))
        assert output == 'undefined'

class TestMultiplier:
    def test_get_next_values(self):
        mult = sm.Multiplier()
        _, output = mult.get_next_values(0, (3, 4))
        assert output == 12

class TestIncrement:
    def test_get_next_values(self):
        inc = sm.Increment()
        state, output = inc.get_next_values(0, 7)
        assert output == 8
        assert state == 8

        state, output = inc.get_next_values(0, 'undefined')
        assert output == 'undefined'
        assert state == 'undefined'

class TestSwitch:
    def test_init(self):
        condition = lambda x: x > 0
        switch = sm.Switch(condition, PlusOne(), MinusOne())
        assert switch.start_state == (0, 0)
        assert switch.condition == condition

    def test_get_next_values(self):
        condition = lambda x: x > 0
        switch = sm.Switch(condition, PlusOne(), MinusOne())

        next_state, output = switch.get_next_values((0, 0), 7)
        assert next_state == (8, 0)
        assert output == 8

        next_state, output = switch.get_next_values((0, 0), -7)
        assert next_state == (0, -8)
        assert output == -8

class TestMux:
    def test_get_next_values(self):
        condition = lambda x: x > 0
        switch = sm.Mux(condition, PlusOne(), MinusOne())

        next_state, output = switch.get_next_values((0, 0), 7)
        assert next_state == (8, 6)
        assert output == 8

        next_state, output = switch.get_next_values((0, 0), -7)
        assert next_state == (-6, -8)
        assert output == -8

class TestMakeCounter:
    def test_make_counter(self):
        counter = sm.make_counter(7, 1)
        assert counter.run(3) == [7, 8, 9]