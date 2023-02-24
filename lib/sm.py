from abc import ABC, abstractmethod

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
                print(f'Current state: {oldsate}, input: {input}, output: {output}, new state: {self.state}')
        return outputs

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

class Cascade(StateMachine):
    def __init__(self, *args):
        super().__init__()
        self.machines = args
        self.start_state = tuple([machine.start_state for machine in self.machines])

    def get_next_values(self, state, input):
        current_input = input
        new_state = ()
        for i in range(len(self.machines)):
            machine = self.machines[i]
            new_state_i, current_input = machine.get_next_values(state[i], current_input)
            new_state = new_state + (new_state_i,)
        return (new_state, current_input)

class SimpleFeedback(StateMachine):
    def __init__(self, machine, first_input):
        super().__init__()
        self.machine = machine
        self.start_state = machine.start_state
        self.first_input = first_input

    def get_next_values(self, state, input):
        new_state, output = self.machine.get_next_values(state, input)
        return (new_state, output)

    def run(self, n=10, verbose=False):
        self.start()
        outputs = []

        current_input = self.first_input
        output = None
        for i in range(n):
            pre_state = self.state
            output = self.step(current_input)
            outputs.append(output)
            if verbose:
                print(f'Step {i}')
                print(f'  {self.__class__.__name__}:')
                print(f'  Input: {current_input}, state: {pre_state} -> {self.state}, output: {output}')

            current_input = output
        return outputs

# A class like SimpleFeedback, but the input is a tuple
class SimpleFeedback2(StateMachine):
    def __init__(self, machine, first_input_tuple):
        super().__init__()
        self.machine = machine
        self.start_state = machine.start_state
        self.first_input = first_input_tuple

    def get_next_values(self, state, input):
        new_state, output = self.machine.get_next_values(state, input)
        return (new_state, output)

    def run(self, n=10, verbose=False):
        self.start()
        outputs = []

        current_input = self.first_input
        output = None
        for i in range(n):
            pre_state = self.state
            output = self.step(current_input)
            outputs.append(output)
            if verbose:
                print(f'Step {i}')
                print(f'  {self.__class__.__name__}:')
                print(f'  Input: {current_input}, state: {pre_state} -> {self.state}, output: {output}')

            current_input = output
        return outputs

class Wire(StateMachine):
    start_state = 0

    def get_next_values(self, _, input):
        return (input, input)

class Delay1(StateMachine):
    def __init__(self, start_state):
        super().__init__()
        self.start_state = start_state

    def get_next_values(self, state, input):
        return (input, state)

class Adder(StateMachine):
    start_state = 0

    def get_next_values(self, state, input):
        return (state, input[0] + input[1])

class FeedbackAdd(StateMachine):
    start_state = 0
    def __init__(self, sm1, sm2):
        super().__init__()
        self.sm1 = sm1
        self.sm2 = sm2

    def get_next_values(self, state, input):
        return (state + input, state + input)