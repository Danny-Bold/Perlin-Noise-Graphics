import sys
import math

from perlin_noise import PerlinNoise
import pygame
import numpy as np
import matplotlib.pyplot as plt


ITERATIONS = 1000
NOISEANGLESCALEFACTOR = math.pi * 5
ACCELSCALEFACTOR = 0.5
VELSCALEFACTOR = 0.1


class Particle:
    def __init__(self, pos):
        self.pos = pos
        self.vel = [0, 0]

    def update(self, noise, zVal):
        noiseVal = noise((*self.pos, zVal)) * NOISEANGLESCALEFACTOR
        self.vel[0] += math.cos(noiseVal) * ACCELSCALEFACTOR
        self.vel[1] += math.sin(noiseVal) * ACCELSCALEFACTOR
        self.pos[0] += self.vel[0] * VELSCALEFACTOR
        self.pos[1] += self.vel[1] * VELSCALEFACTOR

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.pos[0], self.pos[1]), 5)


def main():
    screen = pygame.display.set_mode((1000, 1000))

    noise = PerlinNoise(seed=1, octaves=5)

    grid = [(i * 20, j * 20) for i in range(25) for j in range(25)]

    c = pygame.time.Clock()

    pList = []

    for i in range(10):
        for j in range(10):
            pList.append(Particle([i * 50, j * 50]))

    for iteration in range(ITERATIONS):
        c.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))

        for point in grid:
            noiseAtPoint = noise((*point, iteration / ITERATIONS))
            endcoords = (point[0] + 10 * math.cos(noiseAtPoint * NOISEANGLESCALEFACTOR), point[1] - 10 * math.sin(noiseAtPoint * NOISEANGLESCALEFACTOR))

            pygame.draw.aaline(screen, (255, 255, 255), point, endcoords)

        for p in pList:
            p.draw(screen)
            p.update(noise, iteration / ITERATIONS)

        pygame.display.flip()


if __name__ == '__main__':
    main()
