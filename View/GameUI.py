import pygame
import random

# Init
import Colours
import Settings
from Board import Board
from Connection import Connection
from Particle import Particle
from Player import Player
from Point import Point

pygame.font.init()


class Game:

    # --- Art ---
    missing_texture = pygame.image.load("Art/missing-texture.png") # Placeholder texture
    # Background
    background = missing_texture
    board_background_9x7 = missing_texture
    board_walls_9x7 = missing_texture
    board_background_13x9 = missing_texture
    board_walls_13x9 = missing_texture
    board_background_17x7 = missing_texture
    board_walls_17x7 = missing_texture
    board_background_19x15 = missing_texture
    board_walls_19x15 = missing_texture
    # Banner
    player_left_banner = missing_texture
    waiting_player_banner = missing_texture
    player1_banner = missing_texture
    player2_banner = missing_texture
    you_won_banner = missing_texture
    you_lost_banner = missing_texture
    # Banner buttons
    rematch_button = missing_texture
    leave_button = missing_texture
    # Navigation
    rules_icon = missing_texture
    rules_selected = missing_texture
    exit_icon = missing_texture
    exit_selected = missing_texture
    # Chat
    chat_icon = missing_texture
    chat_selected = missing_texture
    exit_chat = missing_texture
    chat1 = missing_texture
    chat2 = missing_texture
    chat3 = missing_texture
    chat4 = missing_texture
    chat1Selected = missing_texture
    chat2Selected = missing_texture
    chat3Selected = missing_texture
    chat4Selected = missing_texture
    chat1_left = missing_texture
    chat2_left = missing_texture
    chat3_left = missing_texture
    chat4_left = missing_texture
    chat1_right = missing_texture
    chat2_right = missing_texture
    chat3_right = missing_texture
    chat4_right = missing_texture
    # Font
    font = pygame.font.SysFont('arialbold', 30)

    def __init__(self, controller):

        # Players
        self.players = []
        self.players.append(Player("Player One", Colours.PINK))
        self.players[0].turn = True
        self.players.append(Player("Player Two", Colours.YELLOW))

        # Theme
        self.theme = Settings.theme

        self.load_textures()

        # State
        self.is_running = False
        self.chat_active = False

        # Chat state temp
        self.chat_player_id = 0
        self.chat_opponent_id = 0
        self.chat_timer = 0
        self.chat_duration = 60

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Entity variables
        self.myBoard = Board()
        self.current_boardsize = (13, 9)
        self.scale = 1
        self.board_distance = int(50*self.scale)
        self.myBoard.set_board_distance(self.board_distance)
        self.circle_radius = 8
        self.circle_hitbox_multiplier = 1.8
        self.particles = []

        # Buttons
        self.rules_rect = self.rules_icon.get_rect()
        self.chat_rect = self.chat_icon.get_rect()
        self.exit_rect = self.exit_icon.get_rect()
        self.chat_button1_rect = self.chat1.get_rect()
        self.chat_button2_rect = self.chat2.get_rect()
        self.chat_button3_rect = self.chat3.get_rect()
        self.chat_button4_rect = self.chat4.get_rect()
        self.exit_chat_rect = self.exit_chat.get_rect()

        # Chat messages
        self.chat_left_rect = self.chat1_left.get_rect()
        self.chat_right_rect = self.chat1_right.get_rect()

        # Board
        self.background_rect = self.background.get_rect()
        self.board_background_9x7_rect = self.board_background_9x7.get_rect()
        self.board_walls_9x7_rect = self.board_walls_9x7.get_rect()
        self.board_background_13x9_rect = self.board_background_13x9.get_rect()
        self.board_walls_13x9_rect = self.board_walls_13x9.get_rect()
        self.board_background_17x7_rect = self.board_background_17x7.get_rect()
        self.board_walls_17x7_rect = self.board_walls_17x7.get_rect()
        self.board_background_19x15_rect = self.board_background_19x15.get_rect()
        self.board_walls_19x15_rect = self.board_walls_19x15.get_rect()
        self.x_offset = 0
        self.y_offset = 0

        # Banners
        self.player_left_banner_rect = self.player_left_banner.get_rect()
        self.waiting_rect = self.waiting_player_banner.get_rect()
        self.player1_banner_rect = self.player1_banner.get_rect()
        self.player2_banner_rect = self.player2_banner.get_rect()
        self.you_won_banner_rect = self.you_won_banner.get_rect()
        self.you_lost_banner_rect = self.you_lost_banner.get_rect()
        # Banner buttons
        self.rematch_button_rect = self.rematch_button.get_rect()
        self.leave_button_rect = self.leave_button.get_rect()

    def main(self):
        self.event_handler()
        # Ticking
        self.controller.delta_time += self.controller.clock.tick() / 1000.0
        while self.controller.delta_time > 1 / Settings.max_tps:
            self.controller.delta_time -= 1 / Settings.max_tps
            self.update()
            self.render()
            # print(f"TICK: {self.controller.delta_time}")

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.controller.close_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.controller.change_view(self.controller.menuUI)
            elif event.type == pygame.MOUSEBUTTONUP:
                # Particle effect on click
                for i in range(80):
                    loc = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
                    p = Particle(loc, (random.randint(0, 20)/10-1, random.randint(0, 20)/10-1), random.randint(1, 4))
                    self.particles.append(p)

                # Button
                mouse_pos = pygame.mouse.get_pos()
                # Rules
                if self.rules_rect.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.rulesUI)
                # Chat toggle
                if self.chat_rect.collidepoint(mouse_pos):
                    self.chat_active = not self.chat_active
                # Exit
                if self.exit_rect.collidepoint(mouse_pos):
                    self.exit_lobby()
                # Game Over screen
                if self.players[0].score == 3 or self.players[1].score == 3:
                    # Exit
                    if self.leave_button_rect.collidepoint(mouse_pos):
                        self.exit_lobby()
                    # Rematch
                    if self.rematch_button_rect.collidepoint(mouse_pos):
                        self.players[0].score = 0 # eugh, idk, whatever.
                        self.players[1].score = 0 # it just about works since if one quits, the game ends.

                # Chat buttons
                if self.chat_active:
                    if self.chat_button1_rect.collidepoint(mouse_pos):
                        self.controller.client.send_to_server(("!CHAT", 1))
                        self.chat_player_id = 1
                        self.chat_timer = self.chat_duration
                        self.chat_active = False
                    if self.chat_button2_rect.collidepoint(mouse_pos):
                        self.controller.client.send_to_server(("!CHAT", 2))
                        self.chat_player_id = 2
                        self.chat_timer = self.chat_duration
                        self.chat_active = False
                    if self.chat_button3_rect.collidepoint(mouse_pos):
                        self.controller.client.send_to_server(("!CHAT", 3))
                        self.chat_player_id = 3
                        self.chat_timer = self.chat_duration
                        self.chat_active = False
                    if self.chat_button4_rect.collidepoint(mouse_pos):
                        self.controller.client.send_to_server(("!CHAT", 4))
                        self.chat_player_id = 4
                        self.chat_timer = self.chat_duration
                        self.chat_active = False

                # Game logic
                for i in range(self.myBoard.width):
                    for j in range(self.myBoard.height):
                        if self.players[0].turn and self.controller.client.current_population == 2:
                            # Square hitbox points in the board
                            hitbox = pygame.Rect(
                                self.x_offset + i * self.board_distance - self.circle_radius * self.circle_hitbox_multiplier,  # X
                                self.y_offset + j * self.board_distance - self.circle_radius * self.circle_hitbox_multiplier,  # Y
                                self.circle_radius * self.circle_hitbox_multiplier * 2,  # width
                                self.circle_radius * self.circle_hitbox_multiplier * 2  # height
                            )
                            # If point clicked
                            if hitbox.collidepoint(pygame.mouse.get_pos()):
                                point = self.myBoard.points[i][j]
                                point_used = point.is_used
                                player = self.players[0]
                                result = self.myBoard.move(point, player)  # TEMP

                                # Send move to opponent
                                if result:
                                    x = i - (self.myBoard.width-1)
                                    x = -x

                                    self.controller.client.send_to_server(("!MOVE", (x, j)))
                                    # self.controller.client.send_to_server(("!SYNCHRONISE", self.myBoard))

                                # If move made update turn for players
                                if result and not point_used:
                                    player.turn = False
                                    self.players[1].turn = True

                                # Update selected points
                                for row in self.myBoard.points:
                                    for current_point in row:
                                        current_point.is_selected = False
                                point.is_selected = True

    def update(self):

        # Update to current resolution
        # new_scale = self.screen.get_width() / Settings.default_screen_width
        # self.rescale(new_scale)

        # Check for theme change
        if self.theme != Settings.theme:
            self.load_textures()
            self.theme = Settings.theme

        # Layout helper variables
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Buttons
        self.rules_rect.bottomright = (sw-10, sh-20)
        self.chat_rect.bottomleft = (10, sh-20)
        self.chat_button1_rect.bottomleft = (100, sh - 8)
        self.chat_button2_rect.bottomleft = (250, sh - 8)
        self.chat_button3_rect.bottomleft = (400, sh - 8)
        self.chat_button4_rect.bottomleft = (550, sh - 8)
        self.exit_chat_rect.bottomleft = (50, sh-45)
        self.exit_rect.bottomright = (sw-10, sh-20-self.rules_rect.height-20)

        # Background
        self.background_rect.center = (sw/2, sh/2)

        # Board
        self.board_background_9x7_rect.center = (sw / 2, sh / 2)
        self.board_walls_9x7_rect.center = (sw / 2, sh / 2)
        self.board_background_13x9_rect.center = (sw / 2, sh / 2)
        self.board_walls_13x9_rect.center = (sw / 2, sh / 2)
        self.board_background_17x7_rect.center = (sw / 2, sh / 2)
        self.board_walls_17x7_rect.center = (sw / 2, sh / 2)
        self.board_background_19x15_rect.center = (sw / 2, sh / 2)
        self.board_walls_19x15_rect.center = (sw / 2, sh / 2)
        self.x_offset = sw/2 - ((self.myBoard.width-1)/2)*self.board_distance # offset to center the board
        self.y_offset = sh/2 - ((self.myBoard.height-1)/2)*self.board_distance # offset to center the board

        # Banners
        self.waiting_rect.center = (sw/2, sh/2)
        self.player_left_banner_rect.center = (sw / 2, sh / 2)
        self.player1_banner_rect.topleft = (0, 0)
        self.player2_banner_rect.topright = (sw, 0)
        self.you_won_banner_rect.center = (sw / 2, sh / 2)
        self.you_lost_banner_rect.center = (sw / 2, sh / 2)

        # Banner buttons
        self.rematch_button_rect.center = (sw / 2 - 150, sh / 2 + 150)
        self.leave_button_rect.center = (sw / 2 + 150, sh / 2 + 150)

        # Update pending opponent moves
        if self.controller.client.pending_move is not None:
            pending_move = self.controller.client.pending_move
            self.controller.client.pending_move = None
            point = self.myBoard.points[pending_move[0]][pending_move[1]]
            point_used = point.is_used
            result = self.myBoard.move(point, self.players[1])
            for row in self.myBoard.points:
                for current_point in row:
                    current_point.is_selected = False

            # If move made update turn for players
            if result and not point_used:
                self.players[1].turn = False
                self.players[0].turn = True

        if self.controller.client.pending_board is not None:
            pending_board = self.controller.client.pending_board
            self.controller.client.pending_board = None
            self.myBoard = pending_board

        # Check for goal
        for row in self.myBoard.points:
            for current_point in row:
                if current_point.is_goal and current_point.is_ball:
                    if current_point.x < self.myBoard.width/2:
                        self.players[1].score += 1
                    else:
                        self.players[0].score += 1
                    connection_sound = pygame.mixer.Sound('Sound/goal.wav')
                    connection_sound.play()
                    connection_sound.set_volume(0.1)
                    self.myBoard = Board(self.current_boardsize[0], self.current_boardsize[1])

        # Alternative goal: unavailable moves for ball
        if self.myBoard.is_stuck():
            for i in range(len(self.players)):
                self.players[i].score += int(self.players[i].turn == False)
            connection_sound = pygame.mixer.Sound('Sound/goal.wav') # repeating code. put into a new function?
            connection_sound.play()
            connection_sound.set_volume(0.1)
            self.myBoard = Board(self.current_boardsize[0], self.current_boardsize[1])

        # Particles
        self.particles = [particle for particle in self.particles if particle.time > 0]
        for particle in self.particles:
            particle.tick()

        # Size update
        if self.controller.client.board_size is not None:
            self.current_boardsize = self.controller.client.board_size
            self.controller.client.board_size = None
            self.myBoard = Board(self.current_boardsize[0], self.current_boardsize[1])

        # Update chat messages
        if self.chat_timer > 0:
            self.chat_timer -= 1
        else:
            self.chat_player_id = 0
            self.chat_opponent_id = 0

        if self.controller.client.chat_id != 0:
            self.chat_timer = self.chat_duration
            self.chat_opponent_id = self.controller.client.chat_id
            self.controller.client.chat_id = 0
        self.chat_left_rect.topleft = self.player1_banner_rect.bottomleft
        self.chat_right_rect.topright = self.player2_banner_rect.bottomright

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.background, self.background_rect)

        # Draw board background
        if self.current_boardsize == (9,7):
            self.screen.blit(self.board_background_9x7, self.board_background_9x7_rect)
        elif self.current_boardsize == (13,9):
            self.screen.blit(self.board_background_13x9, self.board_background_13x9_rect)
        elif self.current_boardsize == (17, 7):
            self.screen.blit(self.board_background_17x7, self.board_background_17x7_rect)
        elif self.current_boardsize == (19, 15):
            self.screen.blit(self.board_background_19x15, self.board_background_19x15_rect)

        # Draw connections
        for connection in self.myBoard.connections:
            connection.draw(self.screen, (self.x_offset, self.y_offset))

        # Draw board points
        for row in self.myBoard.points:
            for point in row:
                if not point.is_ball:
                    point.draw(self.screen, pygame.mouse.get_pos(), False, (self.x_offset, self.y_offset))

        # Draw board walls
        if self.current_boardsize == (9,7):
            self.screen.blit(self.board_walls_9x7, self.board_background_9x7_rect)
        elif self.current_boardsize == (13,9):
            self.screen.blit(self.board_walls_13x9, self.board_background_13x9_rect)
        elif self.current_boardsize == (17, 7):
            self.screen.blit(self.board_walls_17x7, self.board_background_17x7_rect)
        elif self.current_boardsize == (19, 15):
            self.screen.blit(self.board_walls_19x15, self.board_background_19x15_rect)

        # Draw ball
        for row in self.myBoard.points:
            for point in row:
                if point.is_ball:
                    point.draw(self.screen, pygame.mouse.get_pos(), self.players[0].turn, (self.x_offset, self.y_offset))

        # Draw Player Banner
        self.screen.blit(self.player1_banner, self.player1_banner_rect)
        self.screen.blit(self.player2_banner, self.player2_banner_rect)
        # Draw Score
        font = pygame.font.Font(None, 60)
        score1 = font.render(str(self.players[0].score), True, self.players[0].get_color())
        score1_rect = score1.get_rect()
        score1_rect.center = self.player1_banner_rect.center
        score1_rect[1] += 20
        self.screen.blit(score1, score1_rect)
        score2 = font.render(str(self.players[1].score), True, self.players[1].get_color())
        score2_rect = score1.get_rect()
        score2_rect.center = self.player2_banner_rect.center
        score2_rect[1] += 20
        self.screen.blit(score2, score2_rect)

        # Particles
        for p in self.particles:
            p.draw(self.screen)

        # Waiting banner
        if self.controller.client.current_population == 1:
            self.screen.blit(self.waiting_player_banner, self.waiting_rect)

        if not self.controller.client.connected:
            self.screen.blit(self.player_left_banner, self.player_left_banner_rect)

        # Win condition
        if self.players[0].score == 3:
            self.screen.blit(self.you_won_banner, self.you_won_banner_rect)

        if self.players[1].score == 3:
            self.screen.blit(self.you_lost_banner, self.you_lost_banner_rect)

        # either way, display Rematch and Exit buttons.
        if self.players[0].score == 3 or self.players[1].score == 3:
            self.screen.blit(self.rematch_button, self.rematch_button_rect)
            self.screen.blit(self.leave_button, self.leave_button_rect)


        # Key banner
        if self.controller.client.current_population == 1 and self.controller.client.key is not None:
            # print(self.controller.client.key)
            draw_text("Game Code: "+str(self.controller.client.key), self.font, Colours.WHITE, self.screen, self.screen.get_width()/2-80, 20)

        # Rules icon
        self.screen.blit(self.rules_icon, self.rules_rect)

        # Chat icon
        self.screen.blit(self.chat_icon, self.chat_rect)

        # Exit
        self.screen.blit(self.exit_icon, self.exit_rect)

        # Chat buttons
        if self.chat_active:
            self.screen.blit(self.chat1, self.chat_button1_rect)
            self.screen.blit(self.chat2, self.chat_button2_rect)
            self.screen.blit(self.chat3, self.chat_button3_rect)
            self.screen.blit(self.chat4, self.chat_button4_rect)
            self.screen.blit(self.exit_chat, self.exit_chat_rect)

        # Chat Player1
        if self.chat_player_id == 1:
            self.screen.blit(self.chat1_left, self.chat_left_rect)
        if self.chat_player_id == 2:
            self.screen.blit(self.chat2_left, self.chat_left_rect)
        if self.chat_player_id == 3:
            self.screen.blit(self.chat3_left, self.chat_left_rect)
        if self.chat_player_id == 4:
            self.screen.blit(self.chat4_left, self.chat_left_rect)
        # Chat Player2
        if self.chat_opponent_id == 1:
            self.screen.blit(self.chat1_right, self.chat_right_rect)
        if self.chat_opponent_id == 2:
            self.screen.blit(self.chat2_right, self.chat_right_rect)
        if self.chat_opponent_id == 3:
            self.screen.blit(self.chat3_right, self.chat_right_rect)
        if self.chat_opponent_id == 4:
            self.screen.blit(self.chat4_right, self.chat_right_rect)

        # Button select highlights
        mouse_pos = pygame.mouse.get_pos()
        if self.exit_rect.collidepoint(mouse_pos):
            self.screen.blit(self.exit_selected, (self.exit_rect.x, self.exit_rect.y))
        if self.rules_rect.collidepoint(mouse_pos):
            self.screen.blit(self.rules_selected, (self.rules_rect.x, self.rules_rect.y))
        if self.chat_rect.collidepoint(mouse_pos) and not self.chat_active:
            self.screen.blit(self.chat_selected, (self.chat_rect.x, self.chat_rect.y))
        if self.chat_button1_rect.collidepoint(mouse_pos) and self.chat_active:
            self.screen.blit(self.chat1Selected, (self.chat_button1_rect.x, self.chat_button1_rect.y))
        if self.chat_button2_rect.collidepoint(mouse_pos) and self.chat_active:
            self.screen.blit(self.chat2Selected, (self.chat_button2_rect.x, self.chat_button2_rect.y))
        if self.chat_button3_rect.collidepoint(mouse_pos) and self.chat_active:
            self.screen.blit(self.chat3Selected, (self.chat_button3_rect.x, self.chat_button3_rect.y))
        if self.chat_button4_rect.collidepoint(mouse_pos) and self.chat_active:
            self.screen.blit(self.chat4Selected, (self.chat_button4_rect.x, self.chat_button4_rect.y))

        # Show new frame
        pygame.display.flip()

    def load_textures(self):
        # Path based on current theme
        path = "Art/" + Settings.theme

        # Background
        Game.background = pygame.image.load(path + "/black_bg.png")
        Game.board_background_9x7 = pygame.image.load(path + "/board_background_9x7.png")
        Game.board_walls_9x7 = pygame.image.load(path + "/board_walls_9x7.png")
        Game.board_background_13x9 = pygame.image.load(path + "/board_background_13x9.png")
        Game.board_walls_13x9 = pygame.image.load(path + "/board_walls_13x9.png")
        Game.board_background_17x7 = pygame.image.load(path + "/board_background_17x7.png")
        Game.board_walls_17x7 = pygame.image.load(path + "/board_walls_17x7.png")
        Game.board_background_19x15 = pygame.image.load(path + "/board_background_19x15.png")
        Game.board_walls_19x15 = pygame.image.load(path + "/board_walls_19x15.png")
        # Banner
        Game.player_left_banner = pygame.image.load(path+"/quit.png")
        Game.waiting_player_banner = pygame.image.load(path + "/waiting.png")
        Game.player1_banner = pygame.image.load(path+"/score_player1.png")
        Game.player2_banner = pygame.image.load(path+"/score_player2.png")
        Game.you_won_banner = pygame.image.load(path+"/win.png")
        Game.you_lost_banner = pygame.image.load(path+"/lost.png")
        # Banner buttons
        Game.rematch_button = pygame.image.load(path + "/rematch.png")
        Game.leave_button = pygame.image.load(path + "/quit2.png")
        # Navigation
        Game.rules_icon = pygame.image.load(path+"/question_black.png")
        Game.rules_selected = pygame.image.load(path+"/question_highlight.png")
        Game.exit_icon = pygame.image.load(path+"/exit_door.png")
        Game.exit_selected = pygame.image.load(path+"/exit2_highlight.png")
        # Chat
        Game.chat_icon = pygame.image.load(path+"/chat.png")
        Game.chat_selected = pygame.image.load(path+"/chat_selected.png")
        Game.exit_chat = pygame.image.load(path+"/cross2.png")
        Game.chat1 = pygame.image.load(path+"/chat_wp.png")
        Game.chat2 = pygame.image.load(path+"/chat_hi.png")
        Game.chat3 = pygame.image.load(path+"/chat_bye.png")
        Game.chat4 = pygame.image.load(path+"/chat_gl.png")
        Game.chat1Selected = pygame.image.load(path+"/chat_wp_selected.png")
        Game.chat2Selected = pygame.image.load(path+"/chat_hi_selected.png")
        Game.chat3Selected = pygame.image.load(path+"/chat_bye_selected.png")
        Game.chat4Selected = pygame.image.load(path+"/chat_gl_selected.png")
        Game.chat1_left = pygame.image.load(path+"/left/left_chat_wp.png")
        Game.chat2_left = pygame.image.load(path+"/left/left_chat_hi.png")
        Game.chat3_left = pygame.image.load(path+"/left/left_chat_bye.png")
        Game.chat4_left = pygame.image.load(path+"/left/left_chat_gl.png")
        Game.chat1_right = pygame.image.load(path+"/right/right_chat_wp.png")
        Game.chat2_right = pygame.image.load(path+"/right/right_chat_hi.png")
        Game.chat3_right = pygame.image.load(path+"/right/right_chat_bye.png")
        Game.chat4_right = pygame.image.load(path+"/right/right_chat_gl.png")

        # Ball
        Point.ball_img = pygame.image.load(path+"/ball_green.png")
        # Connections
        Connection.lineHImg = pygame.image.load(path+"/white_neon_hor.png")
        Connection.lineVImg = pygame.transform.rotate(Connection.lineHImg, 90)
        Connection.lineDLImg = pygame.image.load(path+"/white_neon_dia.png")
        Connection.lineDRImg = pygame.transform.flip(Connection.lineDLImg, False, True)
        # Player
        if self.players:
            for player in self.players:
                player.load_textures()

    def exit_lobby(self):
        self.controller.change_view(self.controller.menuUI)
        self.myBoard = Board()
        self.controller.client.disconnect()
        self.players[0].score = 0
        self.players[0].turn = True
        self.players[1].score = 0

    def rescale(self, scale):
        self.scale = scale
        self.board_distance = int(50 * self.scale)
        self.myBoard.set_board_distance(self.board_distance)
        for player in self.players:
            player.lineHImg = pygame.transform.scale(player.lineHImg,(self.board_distance + 15, player.lineHImg.get_height()))
            player.lineVImg = pygame.transform.scale(player.lineVImg, (player.lineVImg.get_width(), self.board_distance + 15))
            player.lineDLImg = pygame.transform.scale(player.lineDLImg, (self.board_distance + 15, self.board_distance + 15))
            player.lineDRImg = pygame.transform.scale(player.lineDRImg, (self.board_distance + 15, self.board_distance + 15))

# Helper function
def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 1, color)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)