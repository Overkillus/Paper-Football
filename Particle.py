import pygame

import Colours


class Particle:
    def __init__(self, location, velocity, time):
        self.location = location
        self.velocity = velocity
        self.time = time

    def draw(self, screen):
        pygame.draw.circle(screen, Colours.WHITE, self.location, self.time)

    def tick(self):
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        self.time -= 0.2
