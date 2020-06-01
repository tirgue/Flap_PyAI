from .Individual import *
import numpy as np
import copy
import random

class Genetic(object):
    
    def __init__(self, nb_population, neuron_network_params):
        self.nb_population = nb_population

        self.population = [None] * nb_population

        for i in range(nb_population):
            self.population[i] = Individual(NeuronNetwork(neuron_network_params[0], neuron_network_params[1], neuron_network_params[2], neuron_network_params[3]))

    def next_gen(self, mutation_rate):
        max = self.fitness_ordering()
        self.bread(max, mutation_rate)

    def fitness_ordering(self):
        self.population.sort(key = lambda ind: ind.fitness, reverse = True)
        total_fitness = 0
        reset = 0
        if self.population[-1].fitness < 0:
            reset = self.population[-1].fitness

        for ind in self.population:
            total_fitness += (ind.fitness - reset)

        self.population[0].fitness_cumulative = (self.population[0].fitness - reset) / total_fitness

        for i in range(1,self.nb_population):
            self.population[i].fitness_cumulative = (self.population[i].fitness - reset) / total_fitness + self.population[i-1].fitness_cumulative

        return copy.deepcopy(self.population)

    def bread(self, individuals, mutation_rate):

        max_chromosomes = self.total_chromosomes() - 1

        for p in range(self.nb_population):
            
            r1 = np.random.uniform()
            r2 = np.random.uniform()

            parent1 = None
            parent2 = None

            i = 0
            while parent1 == None or parent2 == None:
                if parent1 == None and individuals[i].fitness_cumulative >= r1 :
                    parent1 = individuals[i]

                if parent2 == None and individuals[i].fitness_cumulative >= r2 :
                    parent2 = individuals[i]

                i+=1
                 
            bread_point = random.randrange(2, max_chromosomes)

            c = 0

            for l in range(1, self.population[p].neuron_network.number_of_hidden_layers + 2):
                for n in range(self.population[p].neuron_network.layers[l].number_of_neurons):
                    for w in range(self.population[p].neuron_network.layers[l].neurons_weight[n].shape[0]):
                        percent = random.randrange(1, 101, 1)
                        if percent <= mutation_rate:
                            self.population[p].neuron_network.layers[l].neurons_weight[n][w] = 2 * np.random.uniform() - 1
                        
                        else:
                            if c < bread_point:
                                self.population[p].neuron_network.layers[l].neurons_weight[n][w] = parent1.neuron_network.layers[l].neurons_weight[n][w]
                            else:
                                self.population[p].neuron_network.layers[l].neurons_weight[n][w] = parent2.neuron_network.layers[l].neurons_weight[n][w]
                                
                        c += 1

                    percent = random.randrange(1, 101, 1)
                    if percent <= mutation_rate:
                        self.population[p].neuron_network.layers[l].biais = 2 * np.random.uniform() - 1
                    
                    else:
                        if c < bread_point:
                                self.population[p].neuron_network.layers[l].neurons_weight[n][w] = parent1.neuron_network.layers[l].neurons_weight[n][w]
                        else:
                            self.population[p].neuron_network.layers[l].neurons_weight[n][w] = parent2.neuron_network.layers[l].neurons_weight[n][w]

            self.population[p].fitness = 0

    def total_chromosomes(self):
        nn = self.population[0].neuron_network
        rep = 0
        for i in range(1, nn.number_of_hidden_layers + 2):
            w = nn.layers[i].neurons_weight.shape
            rep += w[0]*w[1]

        return rep