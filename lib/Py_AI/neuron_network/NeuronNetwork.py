from .Layer import *

class NeuronNetwork:

    def __init__(self, number_input, number_output, number_of_hidden_layers = 0, length_of_hidden_layers = None):
        
        self.number_of_hidden_layers = number_of_hidden_layers
        self.layers = np.ndarray(number_of_hidden_layers + 2, object)

        # Layer init
        self.layers[0] = Layer(number_input, None)

        for i in range(1, number_of_hidden_layers + 1):
            self.layers[i] = Layer(length_of_hidden_layers[i-1], self.layers[i-1])
            self.layers[i-1].next_layer = self.layers[i]

        self.layers[number_of_hidden_layers + 1] = Layer(number_output, self.layers[number_of_hidden_layers])
        self.layers[number_of_hidden_layers].next_layer = self.layers[number_of_hidden_layers + 1]

    def compute(self, input):
        self.layers[0].activation_value = input

        for i in range(1, self.number_of_hidden_layers + 2):
            self.layers[i].activate_layer()

        return self.layers[-1].activation_value

    def train(self, training_input, training_output):
        result = self.compute(training_input)

        self.layers[-1].delta = (result - training_output) * Sigmoid_dx(self.layers[-1].neurons_value)

        for i in range(self.number_of_hidden_layers, 0, -1):
            self.layers[i].delta = np.dot(self.layers[i + 1].neurons_weight.T, self.layers[i + 1].delta) * Sigmoid_dx(self.layers[i].neurons_value)

        for i in range(1, self.number_of_hidden_layers + 2):
            self.layers[i].neurons_weight = self.layers[i].neurons_weight - np.dot(self.layers[i].delta, self.layers[i - 1].neurons_value.T)
            self.layers[i].biais = self.layers[i].biais - self.layers[i].delta

    @staticmethod
    def normalise(value, max):
        return value * 10 / max - 5
