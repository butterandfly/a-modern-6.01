from abc import ABC, abstractmethod

class StateMachine(ABC):
    start_state = None

    def start(self):
        """To start the state machine.
        """        
        # TODO: set the current state as the start state
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
        # TODO: calculate the new state and output by the getNextValue() function
        state, output = self.get_next_values(self.state, input)

        # TODO: set the current state of this instance as the new state, then return the output
        self.step = state
        return output

    def trnasduce(self, inputs):
        """Step all the inputs.

        Args:
            inputs (List): the input list

        Returns:
            List: the output list
        """
        # TODO: step all the inputs, and return all outputs respectively
        outputs = []
        for input in inputs:
            output = self.step(input)
            outputs.append(output)
        return outputs
