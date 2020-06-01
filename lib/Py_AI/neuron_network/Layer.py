from .math_function.MathFunction import *

class Layer:

    def __init__(self, number_of_neurons, previous_layer):

        self.number_of_neurons = number_of_neurons
        
        self.neurons_value = None

        self.activation_value = None

        self.neurons_weight = None

        self.biais = 2 * np.random.random((number_of_neurons, 1)) - 1

        self.delta = None

        if previous_layer:
            self.neurons_weight = 2 * np.random.uniform(size=(number_of_neurons, previous_layer.number_of_neurons)) - 1 # uses with the previous layer

        self.previous_layer = previous_layer
        self.next_layer = None

    # def activation_value(self):
    #     return Sigmoid(self.neurons_value)

    def activate_layer(self):
        self.neurons_value = np.dot(self.neurons_weight, self.previous_layer.activation_value) + self.biais
        self.activation_value = Sigmoid(self.neurons_value)
