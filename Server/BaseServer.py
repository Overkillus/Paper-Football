import pickle
import socket
import threading

class Server:

    def __init__(self, server, port):
        self.SERVER = server
        self.PORT = port

        # message variables recognised by both client and servers.
        self.HEADER_SIZE = 10
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!GETOUT"
        self.CREATESERVER_MSG = "!CREATESERVER"
        self.JOINSERVER_MSG = "!JOINSERVER"
        self.ENTERGAME_MSG = "!ENTERGAME"
        self.GAMEQUESTION_MSG = "!ISGAME"
        self.QUICKJOINSERVER_MSG = "!QUICKJOIN"
        self.MOVE_MSG = "!MOVE"
        self.SYNCHRONISE_MSG = "!SYNCHRONISE"
        self.POPULATION_MSG = "!POPULATION"
        self.CHAT_MSG = "!CHAT"
        self.PLAYERLEFT_MSG = "!PLAYERLEFT"
        self.BOARDSIZE_MSG = "!BOARDSIZE"

        self.GAMEOVER_STRING = "game over"
        self.GAMETYPE_PUBLIC = "public"
        self.GAMETYPE_PRIVATE = "private"

        self.all_connections = []
        self.SERVER_ON = True # when False, start() stops running.

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.SERVER, self.PORT))

        #self.start()
        t = threading.Thread(target=self.start, args=()) # nice.
        t.start()

    def console(self, msg): # easier output. overridable too.
        print(f"[SERVER-{self.PORT}]:", msg)

    def send_to_client(self, connection, msg):
        # second message - the data
        message = pickle.dumps(msg)
        # first message - the length
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER_SIZE - len(send_len))

        try:
            connection.send(send_len)
            connection.send(message)
        except:
            self.close_connection(connection)
            self.console("message send fail - means connection is dead.")

    def close_connection(self, connection):
        connection.close()
        if connection in self.all_connections:
            self.all_connections.remove(connection)


    # any other specific messages. overriden by children.
    def handle_client_messages(self, connection, address, msg):
        pass

    # handles individual connections
    def handle_client(self, connection, address):
        counter = 0 # just for test purposes. counts individual total of client msgs.
        connected = True
        while connected and connection.fileno() != -1:
            try: # capture client disconnecting prematurely.
                # first message = length of message
                msg_len = connection.recv(self.HEADER_SIZE).decode(self.FORMAT)
                # second message = data
                if msg_len:
                    msg_len = int(msg_len)
                    msg = connection.recv(msg_len)
                    msg = pickle.loads(msg)
                    self.console(f"[{address}] said: {msg}")

                    if msg == self.DISCONNECT_MSG:
                        connected = False
                        self.send_to_client(connection, self.DISCONNECT_MSG)
                        self.console(f"[{address}] has disconnected")
                    # handle any other messages.
                    self.handle_client_messages(connection, address, msg)

                    counter += 1
                    #self.send_to_client(connection, f"msg received ({counter})")
            except:
                connected = False
                self.console(f"Client message error. Connection cut with {address}")

        self.close_connection(connection)


    def send_to_all_clients(self, msg): # e.g. useful for ticks.
        for con in self.all_connections:
            # if connection exists, send. if not, delete it.
            if con.fileno() == -1:
                self.all_connections.remove(con)
            else:
                if msg != None: # useful just to clean up all_connections
                    self.send_to_client(con, msg)

    def send_to_all_clients_except(self, msg, client):
        for con in self.all_connections:
            if con != client:
                # if connection exists, send. if not, delete it.
                if con.fileno() == -1:
                    self.all_connections.remove(con)
                else:
                    if msg != None: # useful just to clean up all_connections
                        self.send_to_client(con, msg)

    # do something to the client once connected. Overriden by children.
    def do_once_client_connected(self, connection):
        pass

    # handles new connections
    def start(self):
        self.sock.listen()
        self.console(f"Hello world! Listening on {self.SERVER}.")
        while self.SERVER_ON:
            connection, address = self.sock.accept()
            self.all_connections.append(connection)
            self.console(f"new connection = {address}")
            self.console(f"connected clients = {len(self.all_connections)}")
            thread = threading.Thread(target=self.handle_client
                                      , args=(connection, address))
            thread.start()
            #self.send_to_all_clients(None) # clean-up all_connections
            self.do_once_client_connected(connection)

#s = Server(socket.gethostname(), 6969)
# you could create a server with this but idk what the point of that is