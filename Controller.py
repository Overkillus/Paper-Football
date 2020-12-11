
import pygame

import Game
import Settings
from UI.MenuUI import MenuUI


class Controller:
    """
    Class managing different views and controlling interactions between modules.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
        pygame.display.set_caption('Paper Football')

        menuUI = MenuUI(self.screen)
        menuUI.main()

    def run(self):
        True

Controller()
