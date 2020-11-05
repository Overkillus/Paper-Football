import sys

import pygame
import numpy as np


class PaperFootball:
    def __init__(self):
        self.width = 500
        self.length = 500
        pygame.init()

        self.screen = pygame.display.set_mode(size=(self.width, self.length))

        while True:
            for event in pygame.event.get():
                if event.type == sys.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
