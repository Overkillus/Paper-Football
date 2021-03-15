from Server.BaseServer import Server
from Server.GameServer import GameServer

class ServerManager(Server):
    def __init__(self, server, port):
        self.SERVERS = {}
        self.SERVER_COUNTER = 0
        self.s = None # for server creation...

        #this runs start(), which halts anything below.
        super().__init__(server, port)

    def remove_empty_servers(self):
        empty_counter = 0
        servers_for_deletion = [] # to delete outside initial for loop.

        for k, serv in self.SERVERS.items():
            self.console(f"{serv}, PLAYERS: {serv.return_players()}")
            if serv.return_players() <= 0 or serv.return_status() == self.GAMEOVER_STRING:
                serv.close_server()
                servers_for_deletion.append(k) # fuhggedaboutit
                empty_counter += 1

        # for loop exceptions when u remove a dictionary item during the loop (fair enough).
        # this da work around.
        for k in servers_for_deletion:
            self.SERVERS.pop(k, None)

        self.console(f"{empty_counter} empty server(s) removed")

    def create_server(self, connection, address, gameType, boardSize):
        self.remove_empty_servers() # a lil extra here: remove empty servers.

        self.console(f"[{address}] wants to create a {gameType} server")
        # create server object. get its key. server should have a STATUS var tbh.
        self.SERVER_COUNTER += 1
        s = GameServer(self.SERVER, self.PORT+self.SERVER_COUNTER, gameType, boardSize)
        k = s.return_key()
        # self.SERVERS.append(s)
        self.SERVERS[k] = s
        # return key to client.
        self.send_to_client(connection, f"{self.JOINSERVER_MSG} {k}")
        # client gets key, and performs join function by themselves automatically.

    def join_server(self, connection, address, msg):
        #self.remove_empty_servers() # slapped here too, why not.

        key = msg[len(self.JOINSERVER_MSG) + 1:]
        self.console(f"[{address}] wants to join ({key})")

        if key in self.SERVERS:
            game_port = self.SERVERS[key].return_port()
            self.console(f"SERVER FOUND FOR PLAYER: {game_port}")
            # hand player the port. now they try to go there themselves.
            self.send_to_client(connection, f"{self.ENTERGAME_MSG} {game_port}")
        else:
            self.console(f"server NOT found for player: {key}")

    def quickjoin_server(self, connection, address, boardSize):
        # send server !QUICKJOIN, and server looks for non-full games. send first one found.
        # if none found, create new server.

        self.remove_empty_servers() # slapped here too, why not.

        server_to_join = 0
        for k, serv in self.SERVERS.items():
            if serv.return_players() < serv.return_max_players() and serv.return_game_type() != self.GAMETYPE_PRIVATE:
                server_to_join = serv.return_port()
                break
        if server_to_join != 0:
            self.send_to_client(connection, f"{self.ENTERGAME_MSG} {server_to_join}")
        else:
            self.create_server(connection, address, self.GAMETYPE_PUBLIC, boardSize)

    # any other specific messages. this overrides the parent one.
    def handle_client_messages(self, connection, address, msg):
        #print("serverManager client message handling. ")
        if self.CREATESERVER_MSG in msg:
            #self.create_server(connection, address, msg[len(self.CREATESERVER_MSG)+1:], (13, 9)) # REPLACE with custom board size
            self.create_server(connection, address, msg[1], msg[2]) # 1 = gameType, 2 = boardsize
        elif self.JOINSERVER_MSG in msg:
            self.join_server(connection, address, msg)
        elif self.QUICKJOINSERVER_MSG in msg:
            self.quickjoin_server(connection, address, msg[1]) # 1 = boardsize. if no game found, it uses this for creation.

# - your code after here! -
server = ServerManager('', 2000)