import sys
import pygame
import Colours
from pygame import mixer
import Settings
# import tkinter as tk  # tkinter is used for GUI. Probably will have to use it at some point for any input

pygame.init()


class SettingsUI:
    """
    Class representing Settings view
    """

    # Art
    background = pygame.image.load("Art/settingsUI.png")
    font = pygame.font.SysFont('arialbold', 30)

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

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
                self.controller.change_view(self.controller.menuUI)
            # Mouse click
            elif event.type == pygame.MOUSEBUTTONUP:
                # Mouse click details
                mouse_pos = pygame.mouse.get_pos()

    def update(self):
        pass

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        # Background
        self.screen.blit(self.background, (0, 0))

        # Show new frame
        pygame.display.flip()

