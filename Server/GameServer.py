import random
import string

from Server.BaseServer import Server


class GameServer(Server):
    def __init__(self, server, port, gameType, boardsize):
        self.STATUS = "running"
        self.PLAYER_COUNT = 0
        self.MAX_PLAYERS = 2
        self.GAME_TYPE = gameType

        # insert boardsize stuff
        self.BOARDSIZE = boardsize # a tuple. e.g. (13, 9) = 13x9

        newKey = ""
        for i in range(6):
            newKey += random.choice(string.digits)
        #print(newKey)
        self.KEY = newKey

        # this runs start(), which halts anything below.
        super().__init__(server, port)

    #
    def handle_client_messages(self, connection, address, msg):
        if self.GAMEQUESTION_MSG in msg:
            self.send_to_client(connection, self.GAMEQUESTION_MSG)
        if self.MOVE_MSG in msg:
            self.send_to_all_clients_except(msg, connection)
        if self.SYNCHRONISE_MSG in msg:
            self.send_to_all_clients(msg)
        if self.POPULATION_MSG in msg:
            self.send_to_all_clients((self.POPULATION_MSG, len(self.all_connections)))
        if self.CHAT_MSG in msg:
            self.send_to_all_clients_except(msg, connection)

    # Overrides the OG close_connection().
    def close_connection(self, connection):
        connection.close()
        if connection in self.all_connections:
            self.all_connections.remove(connection)
        # new additions below
        self.STATUS = self.GAMEOVER_STRING # since a player left, game is dead.
        self.send_to_all_clients_except(self.PLAYERLEFT_MSG, connection)


    def console(self, msg):
        new_msg = (f"[SERVER-{self.PORT}]: {msg}")
        # inspiration for future: send tuples for objects. e.g. (f"[SERVER-{self.PORT}]:", msg)
        #print(new_msg)
        # to make things cleaner, GameServer output are sent to clients.
        self.send_to_all_clients(new_msg)

    def close_server(self): # this function is only useful for gameservers, tbh.
        self.send_to_all_clients(f"{self.ENTERGAME_MSG} {2000}") # exchangeServers(2000)
        self.SERVER_ON = False # close start() thread
        self.STATUS = self.GAMEOVER_STRING

    def do_once_client_connected(self, connection): # overriding the BaseServer version
        self.send_to_client(connection, (self.BOARDSIZE_MSG, self.BOARDSIZE))

    # return functions.
    def return_port(self):
        return self.PORT

    def return_key(self):
        # used to be one time use, but realised that only the server can use this
        return self.KEY

    def return_players(self):
        return len(self.all_connections)

    def return_max_players(self):
        return self.MAX_PLAYERS

    def return_status(self):
        return self.STATUS

    def return_game_type(self):
        return self.GAME_TYPE

    #


# might the infrastructure dif on this one?
# have join and leave functions?
# send_to_game functions?
# if game is full, act as spectator? kick player out?