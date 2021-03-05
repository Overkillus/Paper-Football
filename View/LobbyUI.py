import sys
import pygame
import Settings
import Colours

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
    keypad_join_game = pygame.image.load('Art/join_small.png')
    keypad_join_game_highlight = pygame.image.load('Art/join_small_highlight.png')
    join_random = pygame.image.load('Art/randomgame.png')
    join_random_highlight = pygame.image.load('Art/randomgame_highlight.png')
    create_game = pygame.image.load('Art/createprivate.png')
    create_game_highlight = pygame.image.load('Art/createprivate_highlight.png')
    central_line = pygame.image.load('Art/line_vertical.png')


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
        #self.public_button = game_type_button.copy()
        #self.private_button = game_type_button.copy()

        self.keycode = "" # new LobbyUI variables I just added
        self.server_creation_type = "public"


    def main(self):
        self.event_handler()
        # Ticking
        self.controller.delta_time += self.controller.clock.tick() / 1000.0
        while self.controller.delta_time > 1 / Settings.max_tps:
            self.controller.delta_time -= 1 / Settings.max_tps
            self.update()
            self.render()

    # temporarily slapping LobbyUI function here. it's 6:30am and i cba making new script
    def lobby_buttons(self, action, arg1):
        # self.keycode self.server_creation_type variables placed in init() function.
        if action == "keycode-append" and len(self.keycode) < 5:
            self.keycode += arg1
        elif action == "keycode-erase" and len(self.keycode) > 0:
            self.keycode = self.keycode[:-1]
        elif action == "keycode-reset":
            self.keycode = ""
        elif action == "keycode-join":
            pass #client.join_server(self.keycode)
        elif action == "join-randoms":
            pass #client.quick_join()
        elif action == "public-private":
            self.server_creation_type = arg1
        elif action == "create-server":
            pass #client.create_server()
        print(f"[BUTTON PRESSED] action: {action}, argument: {arg1} | keycode: {self.keycode}, server-creation-type: {self.server_creation_type}")
        # TODO: put this function in a place where the client object can be accessed, or equivalent
        # TODO: art
        # TODO: button changes look on click (both art and code)
        # TODO: display keycode above keypad. BONUS: make the text appear in a stylised font?



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

    def update(self):
        display_x = 100
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        bw = self.keypad_1_button.width + (display_x - self.keypad_1_button.width)
        bh = self.keypad_1_button.height
        y_offset = 0
        x_offset = (self.keypad_1_button.width - display_x) - 0
        rows = 8
        sf = 1.75



        # Exit
        self.exit_button.topleft = (20, 20)

        # keypad
        self.keypad_1_button.center = (sw / sf + display_x, 2 * sh/rows)
        self.keypad_2_button.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows)
        self.keypad_3_button.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows)
        self.keypad_4_button.center = (sw / sf + display_x, 2 * sh / rows + bh + y_offset)
        self.keypad_5_button.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows + bh + y_offset)
        self.keypad_6_button.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + bh + y_offset)
        self.keypad_7_button.center = (sw / sf + display_x, 2 * sh / rows + 2*(bh + y_offset))
        self.keypad_8_button.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows + 2 * (bh + y_offset))
        self.keypad_9_button.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + 2 * (bh + y_offset))
        self.keypad_0_button.center = (sw / sf + bw * 2 + x_offset, 2 * sh / rows + 3 * (bh + y_offset))
        self.keypad_dash_button.center = (sw / sf + display_x, 2 * sh / rows + 3 * (bh + y_offset))
        self.keypad_cancel_button.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + 3 * (bh + y_offset))
        self.keypad_join_game_button.center = (sw / sf + display_x*2 + x_offset, 2 * sh / rows + 4 * (bh + y_offset))
        self.join_random_button.center = (sw/4, sh / 1.5)
        self.create_game_button.center = (sw / 4, sh / 1.25)
        self.central_line_image.center = (sw / 2, sh / 2)
        #self.public_button.center = (sw / 4 - self.create_game.width/4 - 3, sh / 1.5)
        #self.private_button.center = (sw / 4 + self.create_game.width/4 + 2, sh / 1.5)


    def render(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Clear screen
        self.screen.fill((3, 15, 56))

        # Exit Icon
        self.screen.blit(self.exitIcon, self.exit_button)

        # keypad
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

        pygame.display.flip()
