import sys
import pygame
import Settings
import Colours
import time # I'M SORRY

pygame.init()


class LobbyUI:
    """
    Class representing Lobby view
    """

    # Art
    exitIcon = pygame.image.load('Art/exit2.png')
    keypad_1 = pygame.image.load('Art/1.png')
    keypad_1_highlight = pygame.image.load('Art/1_highlight.png')
    keypad_2 = pygame.image.load('Art/2.png')
    keypad_2_highlight = pygame.image.load('Art/2_highlight.png')
    keypad_3 = pygame.image.load('Art/3.png')
    keypad_3_highlight = pygame.image.load('Art/3_highlight.png')
    keypad_4 = pygame.image.load('Art/4.png')
    keypad_4_highlight = pygame.image.load('Art/4_highlight.png')
    keypad_5 = pygame.image.load('Art/5.png')
    keypad_5_highlight = pygame.image.load('Art/5_highlight.png')
    keypad_6 = pygame.image.load('Art/6.png')
    keypad_6_highlight = pygame.image.load('Art/6_highlight.png')
    keypad_7 = pygame.image.load('Art/7.png')
    keypad_7_highlight = pygame.image.load('Art/7_highlight.png')
    keypad_8 = pygame.image.load('Art/8.png')
    keypad_8_highlight = pygame.image.load('Art/8_highlight.png')
    keypad_9 = pygame.image.load('Art/9.png')
    keypad_9_highlight = pygame.image.load('Art/9_highlight.png')
    keypad_0 = pygame.image.load('Art/0.png')
    keypad_0_highlight = pygame.image.load('Art/0_highlight.png')
    keypad_dash = pygame.image.load('Art/dash.png')
    keypad_dash_highlight = pygame.image.load('Art/dash-highlight.png')
    keypad_cancel = pygame.image.load('Art/c.png')
    keypad_cancel_highlight = pygame.image.load('Art/c_highlight.png')
    keypad_join_game = pygame.image.load('Art/join_bigger.png')
    keypad_join_game_highlight = pygame.image.load('Art/join_bigger_highlight.png')
    keypad_screen = pygame.image.load('Art/keypad_screen_small.png')
    join_random = pygame.image.load('Art/randomgame.png')
    join_random_highlight = pygame.image.load('Art/randomgame_highlight.png')
    create_game = pygame.image.load('Art/createprivate.png')
    create_game_highlight = pygame.image.load('Art/createprivate_highlight.png')
    central_line = pygame.image.load('Art/line_vertical.png')

    # options buttons.
    boardsize_1 = pygame.image.load('Art/boardsize_9x7.png')
    boardsize_1_highlight = pygame.image.load('Art/boardsize_9x7_selected.png')
    boardsize_2 = pygame.image.load('Art/boardsize_13x9.png')
    boardsize_2_highlight = pygame.image.load('Art/boardsize_13x9_selected.png')
    boardsize_3 = pygame.image.load('Art/boardsize_17x7.png')
    boardsize_3_highlight = pygame.image.load('Art/boardsize_17x7_selected.png')
    boardsize_4 = pygame.image.load('Art/boardsize_19x15.png')
    boardsize_4_highlight = pygame.image.load('Art/boardsize_19x15_selected.png')

    font = pygame.font.SysFont('arialbold', 50)



    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Exit
        self.exit_button = self.exitIcon.get_rect()

        # keypad
        keypad_button = pygame.Rect(0, 0, 68, 65)
        join_game_button = pygame.Rect(0, 0, keypad_button.width*3.15, keypad_button.height*0.75)
        #game_type_button = pygame.Rect(0, 0, join_game_button.width/2 - 5, join_game_button.height)

        self.keypad_1_button = self.keypad_1.get_rect()
        self.keypad_2_button = self.keypad_2.get_rect()
        self.keypad_3_button = self.keypad_3.get_rect()
        self.keypad_4_button = self.keypad_4.get_rect()
        self.keypad_5_button = self.keypad_5.get_rect()
        self.keypad_6_button = self.keypad_6.get_rect()
        self.keypad_7_button = self.keypad_7.get_rect()
        self.keypad_8_button = self.keypad_8.get_rect()
        self.keypad_9_button = self.keypad_9.get_rect()
        self.keypad_0_button = self.keypad_0.get_rect()
        self.keypad_dash_button = self.keypad_dash.get_rect()
        self.keypad_cancel_button = self.keypad_cancel.get_rect()
        self.keypad_join_game_button = self.keypad_join_game.get_rect()
        self.join_random_button = self.join_random.get_rect()
        self.create_game_button = self.create_game.get_rect()
        self.central_line_image = self.central_line.get_rect()
        self.keypad_screen_image = self.keypad_screen.get_rect()
        #self.public_button = game_type_button.copy()
        #self.private_button = game_type_button.copy()

        # game options
        self.boardsize_1_button = self.boardsize_1.get_rect()
        self.boardsize_2_button = self.boardsize_2.get_rect()
        self.boardsize_3_button = self.boardsize_3.get_rect()
        self.boardsize_4_button = self.boardsize_4.get_rect()

        self.keycode = "" # new LobbyUI variables I just added
        self.server_creation_type = "public"
        self.boardsize_options = [(9,7),(13,9),(17,7),(19,15)]
        self.chosen_boardsize = self.boardsize_options[1]

    def main(self):
        self.event_handler()
        # Ticking
        self.controller.delta_time += self.controller.clock.tick() / 1000.0
        while self.controller.delta_time > 1 / Settings.max_tps:
            self.controller.delta_time -= 1 / Settings.max_tps
            self.update()
            self.render()

    # maybe have a function somewhere for server-joining features?
    def isConnected(self):
        if not self.controller.client.connected:
            self.controller.client.start()
            if self.controller.client.connected:
                return True
            else:
                return False
        else:
            return True

    def waitUntilInGame(self, timeout): # better way on waiting until connected?
        lasttime = time.time()
        while not self.controller.client.IN_GAME and (time.time() - lasttime) < timeout:
            time.sleep(0)  # variable wait, with a max of 2s (aka. timeout)
        return self.controller.client.IN_GAME

    # temporarily slapping LobbyUI function here. it's 6:30am and i cba making new script
    def lobby_buttons(self, action, arg1):
        # self.keycode self.server_creation_type variables placed in init() function.
        if action == "keycode-append" and len(self.keycode) < 6:
            self.keycode += arg1
        elif action == "keycode-erase" and len(self.keycode) > 0:
            self.keycode = self.keycode[:-1]
        elif action == "keycode-reset":
            self.keycode = ""
        elif action == "keycode-join" and self.isConnected():
            self.controller.client.join_server(self.keycode)
            if self.waitUntilInGame(1):
                self.controller.change_view(self.controller.gameUI)
        elif action == "join-randoms" and self.isConnected():
            self.controller.client.quick_join(self.chosen_boardsize)
            self.controller.change_view(self.controller.gameUI)
        elif action == "public-private":
            self.server_creation_type = arg1
        elif action == "create-server" and self.isConnected():
            self.controller.client.create_server(self.controller.client.GAMETYPE_PRIVATE, self.chosen_boardsize)
            self.controller.change_view(self.controller.gameUI)
        print(f"[BUTTON PRESSED] action: {action}, argument: {arg1} | keycode: {self.keycode}, server-creation-type: {self.server_creation_type}")



    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.controller.close_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.controller.change_view(self.controller.menuUI)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                # Back button
                if self.exit_button.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.menuUI)

                # Keypad
                if self.keypad_1_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "1")
                if self.keypad_2_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "2")
                if self.keypad_3_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "3")
                if self.keypad_4_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "4")
                if self.keypad_5_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "5")
                if self.keypad_6_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "6")
                if self.keypad_7_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "7")
                if self.keypad_8_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "8")
                if self.keypad_9_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "9")
                if self.keypad_0_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "0")
                if self.keypad_dash_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-erase", None)
                if self.keypad_cancel_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-reset", None)
                if self.keypad_join_game_button.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-join", None)
                if self.join_random_button.collidepoint(mouse_pos):
                    self.lobby_buttons("join-randoms", None)
                if self.create_game_button.collidepoint(mouse_pos):
                    self.lobby_buttons("create-server", None)
                #if self.public_button.collidepoint(mouse_pos):
                    #self.lobby_buttons("public-private", "public")
                #if self.private_button.collidepoint(mouse_pos):
                    #self.lobby_buttons("public-private", "private")
                if self.boardsize_1_button.collidepoint(mouse_pos):
                    self.chosen_boardsize = (9,7)
                if self.boardsize_2_button.collidepoint(mouse_pos):
                    self.chosen_boardsize = (13,9)
                if self.boardsize_3_button.collidepoint(mouse_pos):
                    self.chosen_boardsize = (17,7)
                if self.boardsize_4_button.collidepoint(mouse_pos):
                    self.chosen_boardsize = (19,15)

    def update(self):
        display_x = self.screen.get_width()/7
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        bw = self.keypad_1_button.width + (display_x - self.keypad_1_button.width)
        bh = self.keypad_1_button.height
        x_offset = (self.keypad_1_button.width - display_x) - 0
        rows = 5
        sf = 1.75



        # Exit
        self.exit_button.topleft = (20, 20)

        # keypad
        self.keypad_1_button.center = (sw / sf + display_x, 2 * sh/rows)
        self.keypad_2_button.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows)
        self.keypad_3_button.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows)
        self.keypad_4_button.center = (sw / sf + display_x, 2 * sh / rows + bh)
        self.keypad_5_button.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows + bh)
        self.keypad_6_button.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + bh)
        self.keypad_7_button.center = (sw / sf + display_x, 2 * sh / rows + 2*bh)
        self.keypad_8_button.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows + 2 * bh)
        self.keypad_9_button.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + 2 * bh)
        self.keypad_0_button.center = (sw / sf + bw * 2 + x_offset, 2 * sh / rows + 3 * bh)
        self.keypad_dash_button.center = (sw / sf + display_x, 2 * sh / rows + 3 * bh)
        self.keypad_cancel_button.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + 3 * bh)
        self.keypad_join_game_button.center = (sw / sf + display_x*2 + x_offset, 2 * sh / rows + 4 * bh)
        self.join_random_button.center = (sw/4, sh / 1.75)
        self.create_game_button.center = (sw / 4, sh / 1.5)
        self.central_line_image.center = (sw / 2, sh / 2)
        self.keypad_screen_image.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows - (self.keypad_screen.get_height() * 0.75))
        #self.public_button.center = (sw / 4 - self.create_game.width/4 - 3, sh / 1.5)
        #self.private_button.center = (sw / 4 + self.create_game.width/4 + 2, sh / 1.5)

        self.boardsize_1_button.center = (self.join_random_button.x, self.keypad_screen_image.y + 60)
        self.boardsize_2_button.center = (self.boardsize_1_button.centerx + self.boardsize_1_button.w + 10, self.boardsize_1_button.centery)
        self.boardsize_3_button.center = (self.boardsize_2_button.centerx + self.boardsize_2_button.w + 10, self.boardsize_1_button.centery)
        self.boardsize_4_button.center = (self.boardsize_3_button.centerx + self.boardsize_3_button.w + 10, self.boardsize_1_button.centery)

    def render(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Clear screen
        self.screen.fill((3, 15, 56))

        # Exit Icon
        self.screen.blit(self.exitIcon, self.exit_button)

        # texts
        draw_text('GAME SELECTION', self.font, Colours.WHITE, self.screen, self.join_random_button.x - 20, self.keypad_screen_image.y - 60)
        draw_text('JOIN LOBBY', self.font, Colours.WHITE, self.screen, self.keypad_screen_image.x + 20, self.keypad_screen_image.y - 60)

        draw_text('Board Size', self.font, Colours.WHITE, self.screen, self.join_random_button.x + 40, self.keypad_screen_image.y)

        # keypad
        draw_text(self.keycode, self.font, Colours.WHITE, self.screen, self.keypad_screen_image.x + 70,
                  self.keypad_screen_image.y + 38)

        self.screen.blit(self.keypad_1, self.keypad_1_button)
        self.screen.blit(self.keypad_2, self.keypad_2_button)
        self.screen.blit(self.keypad_3, self.keypad_3_button)
        self.screen.blit(self.keypad_4, self.keypad_4_button)
        self.screen.blit(self.keypad_5, self.keypad_5_button)
        self.screen.blit(self.keypad_6, self.keypad_6_button)
        self.screen.blit(self.keypad_7, self.keypad_7_button)
        self.screen.blit(self.keypad_8, self.keypad_8_button)
        self.screen.blit(self.keypad_9, self.keypad_9_button)
        self.screen.blit(self.keypad_0, self.keypad_0_button)
        self.screen.blit(self.keypad_dash, self.keypad_dash_button)
        self.screen.blit(self.keypad_cancel, self.keypad_cancel_button)
        self.screen.blit(self.keypad_join_game, self.keypad_join_game_button)
        self.screen.blit(self.join_random, self.join_random_button)
        self.screen.blit(self.create_game, self.create_game_button)
        self.screen.blit(self.central_line, self.central_line_image)
        self.screen.blit(self.keypad_screen, self.keypad_screen_image)

        self.screen.blit(self.boardsize_1, self.boardsize_1_button)
        self.screen.blit(self.boardsize_2, self.boardsize_2_button)
        self.screen.blit(self.boardsize_3, self.boardsize_3_button)
        self.screen.blit(self.boardsize_4, self.boardsize_4_button)

        if self.keypad_1_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_1_highlight, (self.keypad_1_button.x, self.keypad_1_button.y))
        if self.keypad_2_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_2_highlight, (self.keypad_2_button.x, self.keypad_2_button.y))
        if self.keypad_3_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_3_highlight, (self.keypad_3_button.x, self.keypad_3_button.y))
        if self.keypad_4_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_4_highlight, (self.keypad_4_button.x, self.keypad_4_button.y))
        if self.keypad_5_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_5_highlight, (self.keypad_5_button.x, self.keypad_5_button.y))
        if self.keypad_6_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_6_highlight, (self.keypad_6_button.x, self.keypad_6_button.y))
        if self.keypad_7_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_7_highlight, (self.keypad_7_button.x, self.keypad_7_button.y))
        if self.keypad_8_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_8_highlight, (self.keypad_8_button.x, self.keypad_8_button.y))
        if self.keypad_9_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_9_highlight, (self.keypad_9_button.x, self.keypad_9_button.y))
        if self.keypad_0_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_0_highlight, (self.keypad_0_button.x, self.keypad_0_button.y))
        if self.keypad_dash_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_dash_highlight, (self.keypad_dash_button.x, self.keypad_dash_button.y))
        if self.keypad_cancel_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_cancel_highlight, (self.keypad_cancel_button.x, self.keypad_cancel_button.y))
        if self.keypad_join_game_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.keypad_join_game_highlight, (self.keypad_join_game_button.x, self.keypad_join_game_button.y))
        if self.join_random_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.join_random_highlight, (self.join_random_button.x, self.join_random_button.y))
        if self.create_game_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.create_game_highlight, (self.create_game_button.x, self.create_game_button.y))

        if self.chosen_boardsize == self.boardsize_options[0]:
            self.screen.blit(self.boardsize_1_highlight, (self.boardsize_1_button.x, self.boardsize_1_button.y))
        elif self.chosen_boardsize == self.boardsize_options[1]:
            self.screen.blit(self.boardsize_2_highlight, (self.boardsize_2_button.x, self.boardsize_2_button.y))
        elif self.chosen_boardsize == self.boardsize_options[2]:
            self.screen.blit(self.boardsize_3_highlight, (self.boardsize_3_button.x, self.boardsize_3_button.y))
        elif self.chosen_boardsize == self.boardsize_options[3]:
            self.screen.blit(self.boardsize_4_highlight, (self.boardsize_4_button.x, self.boardsize_4_button.y))

        pygame.display.flip()

# Helper Function
def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 1, color)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)
