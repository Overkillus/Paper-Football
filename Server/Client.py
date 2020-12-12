import pickle
import socket
import threading
import time


class Client:
    def __init__(self, server, port):
        self.SERVER = server
        self.PORT = port  # this is the main lobby port.

        self.HEADER_SIZE = 10
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!GETOUT"
        self.CREATESERVER_MSG = "!CREATESERVER"
        self.JOINSERVER_MSG = "!JOINSERVER"
        self.ENTERGAME_MSG = "!ENTERGAME"
        self.GAMEQUESTION_MSG = "!ISGAME"

        self.IN_GAME = False
        self.connected = False
        self.sock = None

        # self.start() # commented out so u can start whenever u like

    # server - client stuff.
    def send_to_server(self, msg):
        # second message - the data
        message = pickle.dumps(msg)
        # first message - the length
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER_SIZE - len(send_len))

        self.sock.send(send_len)
        self.sock.send(message)

    def expect_message(self):
        self.connected = True
        while self.connected:
            # first message = length of message
            msg_len = self.sock.recv(self.HEADER_SIZE).decode(self.FORMAT)
            # second message = data
            if msg_len:
                msg_len = int(msg_len)
                msg = self.sock.recv(msg_len)
                #print(msg_len)
                #print(msg)
                msg = pickle.loads(msg)
                print(f"[SERVER]: {msg}") # test.

                # if statements here for all the actions u want!
                if self.DISCONNECT_MSG in msg:
                    self.connected = False
                    self.console("you've been disconnected.")
                # any other specific messages, send to another function.
                self.handle_server_messages(msg)

    def disconnect(self):
        if self.connected: # maybe slap this in send_to_server instead?
            self.send_to_server(self.DISCONNECT_MSG)

    def console(self, msg):
        print("[CLIENT]:", msg)

    # game server functions.
    def handle_server_messages(self, msg):
        if "[SERVER" in msg: # ignore reposts.
            return

        if self.JOINSERVER_MSG in msg: # end of server creation process.
            key = msg[len(self.JOINSERVER_MSG)+1:] # key received.
            self.console(f"you got the key: {key}")
            self.send_join_server_request(key)
        elif self.ENTERGAME_MSG in msg: # end of server join process
            game_port = msg[len(self.ENTERGAME_MSG)+1:]
            self.console(f"your server port is {game_port}")
            # v basically is starting the client afresh with a new connection really.
            threading.Thread(target=self.exchange_server, args=(game_port,)).start()
        elif self.GAMEQUESTION_MSG in msg: # this is a game server.
            self.IN_GAME = True
            self.console("you're in a game.")

    def send_create_server_request(self):
        self.console("server creation asked. you should join it automatically.")
        self.send_to_server(self.CREATESERVER_MSG)
        # ask ServerManager to create server. have it return key to you.
        # the key is returned and join_server() runs.

    def send_join_server_request(self, key):
        self.console("attempt to join server. if nothing happens, server doesn't exist.")
        self.send_to_server(f"{self.JOINSERVER_MSG} {key}")
        # ask ServerManager to join server with given key. it returns to you the port.
        # you auto join with that port.

    def exchange_server(self, new_port):
        if self.connected:
            self.disconnect()
            # ima keep for now, cuz of weird python message bug when u print after thread
            while self.connected:
                time.sleep(.01)  # wait for the disconnect message from server.

        self.IN_GAME = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.console(f"attempt to join server: {new_port}")
        connect_state = "connecting"
        try:
            self.sock.connect((self.SERVER, int(new_port)))
            connect_state = "connected"
        except:  # cannot connect
            self.console(f"FAILED connecting to server: {new_port}")
            connect_state = "failed"

        if connect_state == "connected":
            # pass state.
            self.console("connected.")
            thread = threading.Thread(target=self.expect_message)
            thread.start()

            time.sleep(0.5)

            self.send_to_server(self.GAMEQUESTION_MSG)  # is this a game?

        else: # return to lobby
            self.exchange_server(self.PORT)  # would this work if it's disconnecting from nothing?

    def start(self):
        self.exchange_server(2000)


# # - your own code after here! -
# client = Client(socket.gethostname(), 2000)
# # just make ^that^ object (with right server and port) and u can do server-client stuff
# client.start()  # you can put this wherever u like
#
#
# # i'm doing a basic menu to showcase entering and leaving the server via ServerManager
# def choice_maker(options):
#     print(f"You have {len(options)} options:")
#     i = 0
#     for o in options:
#         i += 1
#         print(f"\t{i}. {o}")
#     option = input("enter your option: ")
#     try:
#         option = int(option)
#     except:
#         option = 0
#     return option
#
#
# def lobby():
#     option = choice_maker(["Create a server", "Join a server"])
#
#     if option == 1:
#         print("creating server...")
#         client.send_create_server_request()
#     elif option == 2:
#         print("joining server... ")
#         client.send_join_server_request(input("enter the key for that server: "))
#     else:
#         print("invalid option - leaving lobby.")
#         client.disconnect()
#     time.sleep(1)
#
#
# def game():
#     text = input("type whatever u want: ")
#     # if u type !leave, it runs exchange_server(2000)
#     if text == "!leave":
#         client.exchange_server(client.PORT)
#     else:
#         client.send_to_server(text)
#
#     time.sleep(3)
#
#
# while client.connected:
#     if client.IN_GAME:
#         game()
#     else:
#         lobby()
#
# honestly not proud of the use of time.sleep to wait for thread to die and messages to send.
