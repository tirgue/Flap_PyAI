import pygame
import numpy as np
from ..Py_AI.neuron_network.NeuronNetwork import NeuronNetwork
from ..Py_AI.neuron_network.math_function.MathFunction import Sigmoid

class Bird:
    def __init__(self, brain = None):
        self.img = pygame.image.load('lib/Flap/Bird.png')
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width() / 8), int(self.img.get_height() / 8)))
        self.x = 150
        self.y = 250
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.velocity = 0
        self.lifetime = 1
        self.brain = brain
        self.alive = True

    def move(self):
        self.y += self.velocity
        self.velocity = np.min([self.velocity + 2, 20])
        self.lifetime += 1

    def flap(self):
        self.velocity = -20

    def isDead(self, pipe):
        if self.alive:
            if self.y  < 0 or self.y + self.height > 520:
                self.alive = False
                return True

            if self.y  < pipe.y_top or self.y + self.height > pipe.y_bottom:
                if self.x + self.width > pipe.x and self.x  < pipe.x + pipe.width:
                    self.alive = False
                    return True

            return False

        return True

    def think(self, pipe):
        P_TOP = pipe.y_top - self.y
        P_BOT = pipe.y_bottom - self.y
        D_PIPE = pipe.x + pipe.width - self.x

        # P_TOP = NeuronNetwork.normalise(P_TOP, 2)
        # P_BOT = NeuronNetwork.normalise(P_TOP, 2)
        # D_PIPE = NeuronNetwork.normalise(P_TOP, 2)

        result = self.brain.neuron_network.compute([
            [P_TOP],
            [P_BOT],
            [D_PIPE]
        ])

        if result > 0.5:
            self.flap()

    def reset(self):
        self.x = 150
        self.y = 250
        self.lifetime = 1
        self.alive = True

    def draw(self, window):
        pygame.draw.rect(window, (0,0,0), (400,0,200,600))

        window.blit(self.img, (self.x, self.y))
        l = 500
        for layer in self.brain.neuron_network.layers:
            n = 100
            if layer == self.brain.neuron_network.layers[-1]:
                n += 100
            for neuron in layer.activation_value:
                if layer.next_layer == self.brain.neuron_network.layers[-1]:
                    pygame.draw.line(window, (255,255,255), (l, n), (l+100, 200))

                elif layer.next_layer != None:
                    for i in range(1,4):
                        pygame.draw.line(window, (255,255,255), (l, n), (l+100, i*100))

                if layer == self.brain.neuron_network.layers[0]: 
                    r = Sigmoid(neuron[0]) * 255

                else :
                    r = neuron[0] * 255

                pygame.draw.circle(window, (255,255,255), (l, n), 31)
                pygame.draw.circle(window, (r,0,0), (l, n), 30)

                n += 100

            l += 100
        
