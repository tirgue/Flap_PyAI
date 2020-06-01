import pygame
import numpy as np
from lib.Flap.Pipe import Pipe
from lib.Flap.Bird import Bird
from lib.Py_AI.genetic.Genetic import Genetic

screen = pygame.display.set_mode((800,600))
run = True
POPULATION = 10
birds = [None] * POPULATION
pipes = [Pipe()]

background = pygame.image.load('lib/Flap/BG.jpg')
floor = pygame.image.load('lib/Flap/BG_floor.png')
floor_x = 0

clock = pygame.time.Clock()

genetic = Genetic(POPULATION, [3,1,1,np.array([3])])

for i in range(POPULATION):
    birds[i] = Bird(genetic.population[i])


for gen in range(10000):
    print("GENERATION :", gen)
    birds_alive = POPULATION
    pipes = [Pipe()]
    for bird in birds:
        bird.reset()
    while birds_alive > 0 and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if pipes[0].x == 99:
            pipes.append(Pipe())

        if pipes[0].x + pipes[0].width < 0:
            pipes.pop(0)

        screen.blit(background, (0,0))
        for pipe in pipes:
            pipe.move()
            pipe.draw(screen)

        screen.blit(floor, (floor_x,0))
        screen.blit(floor, (floor_x + 400,0))
        pygame.draw.rect(screen, (0,0,0), (400,0,400,600))

        if floor_x < -400:
            floor_x = 400+floor_x

        floor_x -= 3

        birds_alive = 0
        
        for bird in birds:
            if not bird.isDead(pipes[0]):
                bird.brain.fitness = bird.lifetime**2
                bird.think(pipes[0])
                bird.move()
                bird.draw(screen)
                birds_alive += 1

        pygame.display.update()
        clock.tick(35)

    best = genetic.fitness_ordering()
    print("Fitness :", best[0].fitness)

    birds_alive = 100
    genetic.next_gen(5)

    if not run:
        break

pygame.quit()