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

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Exit
        self.exit_button = self.exitIcon.get_rect()

        # keypad
        keypad_button = pygame.Rect(0, 0, 80, 90)
        join_game_button = pygame.Rect(0, 0, keypad_button.width*3.15, keypad_button.height*0.75)
        game_type_button = pygame.Rect(0, 0, join_game_button.width/2 - 5, join_game_button.height)

        self.keypad_1 = keypad_button.copy()
        self.keypad_2 = keypad_button.copy()
        self.keypad_3 = keypad_button.copy()
        self.keypad_4 = keypad_button.copy()
        self.keypad_5 = keypad_button.copy()
        self.keypad_6 = keypad_button.copy()
        self.keypad_7 = keypad_button.copy()
        self.keypad_8 = keypad_button.copy()
        self.keypad_9 = keypad_button.copy()
        self.keypad_delete = keypad_button.copy()
        self.keypad_0 = keypad_button.copy()
        self.keypad_cancel = keypad_button.copy()
        self.join_game = join_game_button.copy()
        self.join_random = join_game_button.copy()
        self.create_game = join_game_button.copy()
        self.public_button = game_type_button.copy()
        self.private_button = game_type_button.copy()

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
                if self.keypad_1.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "1")
                if self.keypad_2.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "2")
                if self.keypad_3.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "3")
                if self.keypad_4.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "4")
                if self.keypad_5.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "5")
                if self.keypad_6.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "6")
                if self.keypad_7.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "7")
                if self.keypad_8.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "8")
                if self.keypad_9.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "9")
                if self.keypad_0.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-append", "0")
                if self.keypad_delete.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-erase", None)
                if self.keypad_cancel.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-reset", None)
                if self.join_game.collidepoint(mouse_pos):
                    self.lobby_buttons("keycode-join", None)
                if self.join_random.collidepoint(mouse_pos):
                    self.lobby_buttons("join-randoms", None)
                if self.create_game.collidepoint(mouse_pos):
                    self.lobby_buttons("create-server", None)
                if self.public_button.collidepoint(mouse_pos):
                    self.lobby_buttons("public-private", "public")
                if self.private_button.collidepoint(mouse_pos):
                    self.lobby_buttons("public-private", "private")

    def update(self):
        display_x = 100
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        bw = self.keypad_1.width + (display_x - self.keypad_1.width)
        bh = self.keypad_1.height
        y_offset = 5
        x_offset = (self.keypad_1.width - display_x) + 5
        rows = 8
        sf = 1.75



        # Exit
        self.exit_button.topleft = (20, 20)

        # keypad
        self.keypad_1.center = (sw / sf + display_x, 2 * sh/rows)
        self.keypad_2.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows)
        self.keypad_3.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows)
        self.keypad_4.center = (sw / sf + display_x, 2 * sh / rows + bh + y_offset)
        self.keypad_5.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows + bh + y_offset)
        self.keypad_6.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + bh + y_offset)
        self.keypad_7.center = (sw / sf + display_x, 2 * sh / rows + 2*(bh + y_offset))
        self.keypad_8.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows + 2 * (bh + y_offset))
        self.keypad_9.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + 2 * (bh + y_offset))
        self.keypad_delete.center = (sw / sf + display_x, 2 * sh / rows + 3 * (bh + y_offset))
        self.keypad_0.center = (sw / sf + bw*2 + x_offset, 2 * sh / rows + 3 * (bh + y_offset))
        self.keypad_cancel.center = (sw / sf + bw*3 + x_offset*2, 2 * sh / rows + 3 * (bh + y_offset))
        self.join_game.center = (sw / sf + display_x*2 + x_offset, 2 * sh / rows + 4 * (bh + y_offset))
        self.join_random.center = (sw/4, sh / 5)
        self.create_game.center = (sw / 4, sh / 1.25)
        self.public_button.center = (sw / 4 - self.create_game.width/4 - 3, sh / 1.5)
        self.private_button.center = (sw / 4 + self.create_game.width/4 + 2, sh / 1.5)


    def render(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Clear screen
        self.screen.fill((255, 182, 193))

        # Exit Icon
        self.screen.blit(self.exitIcon, self.exit_button)

        # keypad
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_1)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_2)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_3)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_4)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_5)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_6)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_7)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_8)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_9)
        pygame.draw.rect(self.screen, Colours.RED, self.keypad_delete)
        pygame.draw.rect(self.screen, Colours.GREY, self.keypad_0)
        pygame.draw.rect(self.screen, Colours.RED, self.keypad_cancel)
        pygame.draw.rect(self.screen, Colours.GREEN, self.join_game)
        pygame.draw.rect(self.screen, Colours.CYAN, self.join_random)
        pygame.draw.rect(self.screen, Colours.PURPLE, self.create_game)
        pygame.draw.rect(self.screen, Colours.ORANGE, self.public_button)
        pygame.draw.rect(self.screen, Colours.YELLOW, self.private_button)

        pygame.display.flip()
