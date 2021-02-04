from Server.BaseServer import Server
from Server.GameServer import GameServer
from Server.ServerManager import ServerManager
from Server.Client import Client

import time
import socket

import unittest
from test import support

class TestCase1(unittest.TestCase):
    def setUp(self):
        self.serverManager = ServerManager(socket.gethostname(), 2000)
        #self.gameServer = GameServer(socket.gethostname(), 2001)
        self.client = Client(socket.gethostname(), 2000)

    def tearDown(self):
        pass
        # server and client disconnect?

    # since these tests are asynchronous, waiting is required at times.

    def test1(self): # client connect
        self.client.start()

    def test2(self): # client create server. this performs the join too.
        self.client.create_server()

    def test3(self): # client leave server
        self.client.disconnect()

    def test4(self): # client join non-existent server
        self.client.join_server("AAAAAA")

    def test5(self): # client sends pointless message
        self.client.send_to_server("jv(w$jowjty($")

if __name__ == '__main__':
    unittest.main()

