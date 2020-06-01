from ..neuron_network.NeuronNetwork import *

class Individual(object):
    
    def __init__(self, neuron_network):
        self.neuron_network = neuron_network
        self.fitness = 1
        self.fitness_cumulative = 0