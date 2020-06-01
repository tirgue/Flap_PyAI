import random
import pygame

class Pipe:
    def __init__(self):
        self.img = pygame.image.load('lib/Flap/Pipe.png')
        self.x = 450
        self.y_bottom = random.randint(250, 500)
        self.y_top = self.y_bottom - 200
        self.width = self.img.get_width()

    def move(self):
        self.x -= 3

    def reset(self):
        self.x = 450

    def draw(self, window):
        window.blit(pygame.transform.flip(self.img, False, True), (self.x, self.y_top - self.img.get_height()))
        window.blit(self.img, (self.x, self.y_bottom))
