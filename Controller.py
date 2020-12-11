
import pygame


import Settings
from UI import MenuUI


class Controller:
    """
    Class managing different views and controlling interactions between modules.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
        pygame.display.set_caption('Paper Football')
        MenuUI.main_menu()

Controller()
