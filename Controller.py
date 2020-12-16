import socket
import sys

import pygame

from Server.Client import Client
from View.Game import Game
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
        self.screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
        pygame.display.set_caption('Paper Football')

        # # State
        # self.in_session = False

        # Client (connection)
        self.client = Client(socket.gethostname(), 2000)  # TODO temp local ip address
        # self.client = Client("139.162.219.137", 2000)
        # self.client.start()  #temp

        # Clock
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Views
        self.menuUI = MenuUI(self)
        self.game = Game(self)
        self.settingsUI = SettingsUI(self)
        self.rulesUI = RulesUI(self)
        self.views = [self.menuUI, self.game, self.settingsUI, self.rulesUI]

        # Initial state
        self.menuUI.is_running = True

        # Start
        self.run()

    def run(self):
        while True:
            for view in self.views:
                if view.is_running:
                    view.main()

    def close_game(self):
        if self.client.connected:
            self.client.disconnect()
        sys.exit(0)

    def change_view(self, view):
        if view not in self.views:
            return False
        else:
            for v in self.views:
                v.is_running = False
            view.is_running = True


Controller()
