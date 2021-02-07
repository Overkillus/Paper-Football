from Server.BaseServer import Server
from Server.GameServer import GameServer
from Server.ServerManager import ServerManager
from Server.Client import Client

import time
import socket

import unittest
from test import support

#serverManager = ServerManager(socket.gethostname(), 2000)
# gameServer = GameServer(socket.gethostname(), 2001)
#client = Client(socket.gethostname(), 2000)

class TestCase1(unittest.TestCase):
    # I think this script only works when run in isolation with just the Server folder.
    # anything else and the socket will be used by other scripts.

    def setUp(self): # run at start of every test
        self.serverManager = ServerManager(socket.gethostname(), 2000)
        # gameServer = GameServer(socket.gethostname(), 2001)
        self.client = Client(socket.gethostname(), 2000)
        pass

    def tearDown(self): # run at end of every test
        #self.client.disconnect()
        self.serverManager.SERVER_ON = False # closes server. THIS IS UGLY, MAKE A FUNC FOR THIS SOON.
        time.sleep(0.5)
        pass
        # server and client disconnect? closing both connections?

    # since these tests are asynchronous, waiting is required at times.

    def test1(self): # client connect
        self.client.start()

    def test2(self): # client create server. this performs the join too.
        self.client.create_server()

"""
    def test3(self): # client leave server
        self.client.disconnect()

    def test4(self): # client join non-existent server
        self.client.join_server("AAAAAA")

    def test5(self): # client sends pointless message
        self.client.send_to_server("jv(w$jowjty($")
"""

if __name__ == '__main__':
    unittest.main()

