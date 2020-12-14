import socket
import sys

import pygame

from Server.Client import Client
from View.Game import Game
import Settings
from View.MenuUI import MenuUI

pygame.init()


class Controller:
    """
    Class managing different views and controlling interactions between modules.
    """
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
        pygame.display.set_caption('Paper Football')

        # Client (connection)
        self.client = Client(socket.gethostname(), 2000)  # TODO temp local ip address
        # self.client.start()  #temp

        # Clock
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Views
        self.menuUI = MenuUI(self)
        self.game = Game(self)

        # Initial state
        self.menuUI.is_running = True

        # Start
        self.run()

    def run(self):
        while True:
            if self.menuUI.is_running:
                self.menuUI.main()
            if self.game.is_running:
                self.game.main()

    def close_game(self):
        if self.client.connected:
            self.client.disconnect()
        sys.exit(0)


Controller()
