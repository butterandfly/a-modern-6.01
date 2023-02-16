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
