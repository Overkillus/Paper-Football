import socket
import sys

import pygame

from Server.Client import Client
from View.GameUI import Game
import Settings
from View.MenuUI import MenuUI
from View.SettingsUI import SettingsUI
from View.RulesUI import RulesUI

pygame.init()


class Controller:
    """
    Class managing different views and controlling interactions between modules.
    """
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption('Paper Football')

        # self.client = Client(socket.gethostname(), 2000)
        self.client = Client("139.162.219.137", 2000) # Server ip

        # Clock
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Views
        self.menuUI = MenuUI(self)
        self.gameUI = Game(self)
        self.settingsUI = SettingsUI(self)
        self.rulesUI = RulesUI(self)
        self.views = [self.menuUI, self.gameUI, self.settingsUI, self.rulesUI]

        # Initial state
        self.menuUI.is_running = True

        # Start
        self.run()

    # Show the currently active view (1 at a time)
    def run(self):
        while True:
            for view in self.views:
                if view.is_running:
                    view.main()

    # Terminate server connection and close application
    def close_game(self):
        if self.client.connected:
            self.client.disconnect()
        sys.exit(0)

    # Swap current view
    def change_view(self, view):
        if view not in self.views:
            return False
        else:
            for v in self.views:
                v.is_running = False
            view.is_running = True


# Self-activation
Controller()
