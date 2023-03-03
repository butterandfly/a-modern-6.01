from abc import ABC, abstractmethod
from typing import Callable

class StateMachine(ABC):
    start_state = None
    state = None

    def start(self):
        """To start the state machine.
        """        
        # Set the current state as the start state
        self.state = self.start_state

    @abstractmethod
    def get_next_values(self, state, input):
        """To get the next state and ouput by the state and input.

        Args:
            state (_type_): the state
            input (_type_): the input

        Returns:
            tuple: contains the calculated state and output
        """

        pass

    def step(self, input):
        """Go to the next state by the input.

        Args:
            input (_type_): a SM input

        Returns:
            _type_: the output calculated by the input and current state
        """
        # Calculate the new state and output by the getNextValue() function
        state, output = self.get_next_values(self.state, input)

        # Set the current state of this instance as the new state, then return the output
        self.state = state
        return output

    def transduce(self, inputs, verbose=False):
        """Start from the start state, step all inputs.

        Args:
            inputs (List): the input list

        Returns:
            List: the output list
        """
        self.start()

        # Print the beginning state if verbose is True
        if verbose:
            print(f'Start at: {self.state}')

        # step all the inputs, and return all outputs respectively
        outputs = []
        for input in inputs:
            oldsate = self.state
            output = self.step(input)
            outputs.append(output)
            # Print information if verbose is True
            if verbose:
                print(f'Input: {input}, state: {oldsate} -> {self.state}, output: {output}')
        return outputs

    def run(self, n=10, verbose=False):
        inputs = ['undefined'] * n
        return self.transduce(inputs, verbose)


class Parallel(StateMachine):
    def __init__(self, *args):
        super().__init__()
        self.machines = args
        self.start_state = tuple([machine.start_state for machine in self.machines])

    def get_next_values(self, state, input):
        new_states = []
        outputs = []
        for i in range(len(self.machines)):
            machine = self.machines[i]
            new_state, output = machine.get_next_values(state[i], input)
            new_states.append(new_state)
            outputs.append(output)
        return (tuple(new_states), tuple(outputs))

class ParallelAdd(StateMachine):
    start_state: tuple
    def __init__(self, sm1: StateMachine, sm2: StateMachine):
        self.sm1 = sm1
        self.sm2 = sm2
        self.start_state = (sm1.start_state, sm2.start_state)

    def get_next_values(self, state: tuple, input: any):
        s1, o1 = self.sm1.get_next_values(state[0], input)
        s2, o2 = self.sm2.get_next_values(state[1], input)
        return ((s1, s2), o1 + o2)

class Cascade(StateMachine):
    def __init__(self, sm1, sm2):
        super().__init__()
        self.sm1 = sm1
        self.sm2 = sm2
        self.start_state = (sm1.start_state, sm2.start_state)

    def get_next_values(self, state, input):
        s1, o1 = self.sm1.get_next_values(state[0], input)
        s2, o2 = self.sm2.get_next_values(state[1], o1)
        return ((s1, s2), o2)

class Feedback(StateMachine):
    def __init__(self, sm):
        super().__init__()
        self.sm = sm
        self.start_state = sm.start_state

    def get_next_values(self, state, input):
        _, output = self.sm.get_next_values(state, 'undefined')
        new_state, _ = self.sm.get_next_values(state, output)
        return (new_state, output)

class Feedback2(StateMachine):
    def __init__(self, sm):
        super().__init__()
        self.sm = sm
        self.start_state = sm.start_state

    def get_next_values(self, state, input):
        _, output = self.sm.get_next_values(state, (input, 'undefined'))
        new_state, _ = self.sm.get_next_values(state, (input, output))
        return (new_state, output)

class FeedbackAdd(StateMachine):
    def __init__(self, sm1, sm2):
        super().__init__()
        self.sm1 = sm1
        self.sm2 = sm2
        self.start_state = (sm1.start_state, sm2.start_state)

    def get_next_values(self, state, input):
        _, o1 = self.sm1.get_next_values(state[0], 'undefined')
        s2, o2 = self.sm2.get_next_values(state[1], o1)
        s1, output = self.sm1.get_next_values(state[0], (input+o2))
        return ((s1, s2), output)

class Wire(StateMachine):
    start_state = 0

    def get_next_values(self, _, input):
        return (input, input)

class Delay(StateMachine):
    def __init__(self, start_state):
        super().__init__()
        self.start_state = start_state

    def get_next_values(self, state, input):
        return (input, state)

class Gain(StateMachine):
    def __init__(self, gain):
        super().__init__()
        self.gain = gain

    def get_next_values(self, _, input):
        return (input, input * self.gain)

class Increment(StateMachine):
    start_state = 0

    def __init__(self, step=1):
        super().__init__()
        self.step = step

    def get_next_values(self, _, input):
        if input == 'undefined':
            return ('undefined', 'undefined')
        output = input + self.step
        return (output, output)

class Adder(StateMachine):
    start_state = 0

    def get_next_values(self, state, input):
        if 'undefined' in input:
            return ('undefined', 'undefined')

        output = input[0] + input[1]
        return (output, output)

class Multiplier(StateMachine):
    start_state = 1
    def get_next_values(self, _, input):
        if 'undefined' in input:
            return ('undefined', 'undefined')

        output = input[0] * input[1]
        return (output, output)

class Switch(StateMachine):
    def __init__(self, condition: Callable, sm1: StateMachine, sm2: StateMachine):
        super().__init__()
        self.sm1 = sm1
        self.sm2 = sm2
        self.condition = condition
        self.start_state = (sm1.start_state, sm2.start_state)

    def get_next_values(self, state, input):
        if self.condition(input):
            s1, o1 = self.sm1.get_next_values(state[0], input)
            return ((s1, state[1]), o1)
        else:
            s2, o2 = self.sm2.get_next_values(state[1], input)
            return ((state[0], s2), o2)

class Mux(Switch):
    def get_next_values(self, state, input):
        s1, o1 = self.sm1.get_next_values(state[0], input)
        s2, o2 = self.sm2.get_next_values(state[1], input)
        if self.condition(input):
            return ((s1, s2), o1)
        else:
            return ((s1, s2), o2)

class If(StateMachine):
    start_state = ('start', None)

    def __init__(self, condition, sm1, sm2) -> None:
        super().__init__()
        self.condition = condition
        self.sm1 = sm1
        self.sm2 = sm2

    def get_first_real_state(self, input):
        if self.condition(input):
            return ('running_sm1', self.sm1.start_state)
        else:
            return ('running_sm2', self.sm2.start_state)

    def get_next_values(self, state, input):
        if_state, sm_state = state
        if if_state == 'start':
            if_state, sm_state = self.get_first_real_state(input)
        
        if if_state == 'running_sm1':
            new_sm_state, output = self.sm1.get_next_values(sm_state, input)
        else:
            new_sm_state, output = self.sm2.get_next_values(sm_state, input)

        return ((if_state, new_sm_state), output)

def make_counter(start_number, step=1):
    return Feedback(Cascade(Increment(step), Delay(start_number)))

R = Delay