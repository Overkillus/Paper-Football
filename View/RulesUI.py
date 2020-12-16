import sys
import pygame
from View import Game
import Colours
from pygame import mixer
import Settings
# import tkinter as tk  # tkinter is used for GUI. Probably will have to use it at some point for any input

pygame.init()


class RulesUI:
    """
    Class representing Rules view
    """

    # Art
    font = pygame.font.SysFont('arialbold', 30)
    rules_icon = pygame.image.load("Art/question_black.png")

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller
        self.rules_rect = self.rules_icon.get_rect(topleft=(630, 430))

    def main(self):
        self.event_handler()
        # Ticking
        self.controller.delta_time += self.controller.clock.tick() / 1000.0
        while self.controller.delta_time > 1 / Settings.max_tps:
            self.controller.delta_time -= 1 / Settings.max_tps
            self.update()
            self.render()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.controller.close_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.controller.change_view(self.controller.game)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.rules_rect.collidepoint(pygame.mouse.get_pos()):
                    self.controller.change_view(self.controller.game)

    def update(self):
        pass

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 255))
        self.screen.blit(self.rules_icon, (630, 430))

        # Show new frame
        pygame.display.flip()

