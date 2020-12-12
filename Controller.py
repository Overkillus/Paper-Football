import pygame
from Game import Game
import Settings
from UI.MenuUI import MenuUI

pygame.init()


class Controller:
    """
    Class managing different views and controlling interactions between modules.
    """
    clock = pygame.time.Clock()
    delta_time = 0

    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
        pygame.display.set_caption('Paper Football')

        self.menuUI = MenuUI(self.screen, self)
        MenuUI.is_running = True

        self.game = Game(self.screen, self)

        self.run()

    def run(self):
        while True:
            if self.menuUI.is_running:
                self.menuUI.main()
            if self.game.is_running:
                self.game.main()


Controller()
