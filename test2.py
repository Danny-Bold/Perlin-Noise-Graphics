import sys
import math
import random

from perlin_noise import PerlinNoise
import pygame
import numpy as np

"""

This file gradually improves on the simulation developed while removing image/video generation.

"""

ALPHA = 0.4  # How opaque should the particle trails be? 0 = transparent, 1 = opaque

ITERATIONS = 600  # number of frames to run the simulation for

NOISEANGLESCALEFACTOR = math.pi * 5
ACCELSCALEFACTOR = 0.2
VELSCALEFACTOR = 0.1

DIMENSION = (1000, 1000)

NOOFPARTICLES = 50

STROKE = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1), (2, 0), (-2, 0), (0, 2), (0, -2)]

# SEED = random.randint(0, 2000)
SEED = 1666
OCTAVES = 1

print('Seed: ', SEED)
random.seed(SEED)


class Canvas:
    def __init__(self, size):
        self.size = size
        self.array = np.zeros((*size, 3))
        self.surface = pygame.Surface(size)

    def addPixel(self, p):
        sP = pygame.PixelArray(self.surface)

        pos = (round(p.pos[0]), round(p.pos[1]))

        try:
            for point in STROKE:
                for i in range(3):
                    self.array[pos[0] + point[0], pos[1] + point[1], i] += ALPHA * p.col[i]
                    self.array[pos[0] + point[0], pos[1] + point[1], i] = min(self.array[pos[0] + point[0], pos[1] + point[1], i], 1)  # update canvas

                sP[pos[0] + point[0], pos[1] + point[1]] = (self.array[pos[0] + point[0], pos[1] + point[1], 0] * 255, self.array[pos[0] + point[0], pos[1] + point[1], 1] * 255,
                                          self.array[pos[0] + point[0], pos[1] + point[1], 2] * 255)

            del sP

        except:
            pass

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))


class Particle:
    def __init__(self, pos=(0, 0), vel=(0, 0), startHue=0):
        """

        Ensure col[i] < 1!

        """
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.colObj = pygame.color.Color(0, 0, 0)
        self.hue = startHue
        self.colObj.hsva = (startHue, 100, 100, 0)
        self.col = (self.colObj.r / 255, self.colObj.g / 255, self.colObj.g / 255)

    def update(self, noise, zVal, screenSize=(500, 500)):

        noiseVal = noise((self.pos[0] / screenSize[0], self.pos[1] / screenSize[1], zVal)) * NOISEANGLESCALEFACTOR
        self.vel[0] += math.cos(noiseVal) * ACCELSCALEFACTOR
        self.vel[1] += math.sin(noiseVal) * ACCELSCALEFACTOR

        self.pos[0] += self.vel[0] * VELSCALEFACTOR
        self.pos[1] += self.vel[1] * VELSCALEFACTOR

        if self.pos[0] > screenSize[0] - 1:
            self.pos[0] -= screenSize[0] - 1

        if self.pos[0] < 0:
            self.pos[0] += screenSize[0] - 1

        if self.pos[1] > screenSize[1] - 1:
            self.pos[1] -= screenSize[1] - 1

        if self.pos[1] < 0:
            self.pos[1] += screenSize[1] - 1

        self.hue += 1
        self.hue = self.hue % 360
        self.colObj.hsva = (self.hue, 100, 100, 0)
        self.col = (self.colObj.r / 255, self.colObj.g / 255, self.colObj.b / 255)


def posToHue(pos):
    return ((pos[0] + pos[1]) * 360 / pos[0]) % 360


def main(screen):

    canvas = Canvas(DIMENSION)

    pList = []

    for i in range(NOOFPARTICLES):
        startPos = (random.randint(0, DIMENSION[0] - 1), random.randint(0, DIMENSION[1] - 1))
        pList.append(Particle(pos=(random.randint(0, DIMENSION[0] - 1), random.randint(0, DIMENSION[1] - 1)),
                              startHue=posToHue(startPos)))

    noise = PerlinNoise(seed=SEED, octaves=OCTAVES)

    c = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        c.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        for p in pList:
            canvas.addPixel(p)
            p.update(noise, iteration / ITERATIONS, screenSize=DIMENSION)

        canvas.draw(screen)

        pygame.display.flip()


def buffer():

    screen = pygame.display.set_mode(DIMENSION)

    end = False

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end = True

        pygame.display.flip()

    main(screen)


if __name__ == '__main__':
    buffer()
