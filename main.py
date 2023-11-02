import sys
import math

from perlin_noise import PerlinNoise
import pygame
import numpy as np
import matplotlib.pyplot as plt

"""

Now, add gradually changing hue.

"""

ALPHA = 0.4  # How opaque should the particle trails be? 0 = transparent, 1 = opaque

ITERATIONS = 1000  # number of frames to run the simulation for

NOISEANGLESCALEFACTOR = math.pi * 5
ACCELSCALEFACTOR = 0.2
VELSCALEFACTOR = 0.1

DIMENSION = (5000, 5000)


STROKE = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]


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


def main():
    screen = pygame.display.set_mode(DIMENSION)
    canvas = Canvas(DIMENSION)

    pList = []

    for i in range(100):
        for j in range(100):
            pList.append(Particle(pos=(50 * i, 50 * j), startHue=0))

    noise = PerlinNoise(seed=1, octaves=3)

    c = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        c.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                plt.imsave('imgtemp/imgtemp.png', canvas.array)
                sys.exit()

        for p in pList:
            canvas.addPixel(p)
            p.update(noise, iteration / ITERATIONS, screenSize=DIMENSION)

        canvas.draw(screen)

        pygame.display.flip()

    plt.imsave('imgtemp/imgtemp.png', canvas.array)


if __name__ == '__main__':
    main()
