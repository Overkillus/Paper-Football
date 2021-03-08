import sys
import pygame
import random

# Init
import Colours
import Settings
from Board import Board
from Particle import Particle
from Player import Player
from Point import Point


class Game:

    # Art
    boardImg = pygame.image.load("Art/board_lines.png")
    boardWalls = pygame.image.load("Art/board_walls.png")
    waitingPlayer = pygame.image.load("Art/waiting.png")
    rules_icon = pygame.image.load("Art/question_black.png")
    chat_icon = pygame.image.load("Art/chat.png")
    exit_icon = pygame.image.load("Art/exit_door.png")
    player1_banner = pygame.image.load("Art/score_player1.png")
    player2_banner = pygame.image.load("Art/score_player2.png")

    exit_selected = pygame.image.load("Art/exit2_highlight.png")
    rules_selected = pygame.image.load("Art/question_highlight.png")
    chat_selected = pygame.image.load("Art/chat_selected.png")
    chat1 = pygame.image.load("Art/well_played.png")
    chat2 = pygame.image.load("Art/nice_move.png")
    chat3 = pygame.image.load("Art/good_luck.png")
    chat1Selected = pygame.image.load("Art/well_played_selected.png")
    chat2Selected = pygame.image.load("Art/nice_move_selected.png")
    chat3Selected = pygame.image.load("Art/good_luck_selected.png")
    exit_chat = pygame.image.load("Art/cross2.png")

    def __init__(self, controller):
        # State
        self.is_running = False
        self.chatActive = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Entity variables
        self.myBoard = Board(Settings.board_width, Settings.board_height)
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
        self.exit_chat_rect = self.exit_chat.get_rect()

        # Board
        self.board_lines_rect = self.boardImg.get_rect()
        self.board_walls_rect = self.boardWalls.get_rect()
        self.x_offset = 0
        self.y_offset = 0

        # Banners
        self.waiting_rect = self.waitingPlayer.get_rect()
        self.player1_banner_rect = self.player1_banner.get_rect()
        self.player2_banner_rect = self.player2_banner.get_rect()

        # Players
        self.players = []
        self.players.append(Player("Player One", Colours.PINK))
        self.players[0].turn = True
        self.players.append(Player("Player Two", Colours.YELLOW))

    def main(self):
        self.event_handler()
        # Ticking
        self.controller.delta_time += self.controller.clock.tick() / 1000.0
        while self.controller.delta_time > 1 / Settings.max_tps:
            self.controller.delta_time -= 1 / Settings.max_tps
            self.update()
            self.render()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.controller.close_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.controller.change_view(self.controller.menuUI)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q: # TODO add a button and generalize
                self.controller.change_view(self.controller.menuUI)
                self.myBoard = Board()
                self.controller.client.disconnect()
                self.players[0].score = 0
                self.players[0].turn = True
                self.players[1].score = 0
            elif event.type == pygame.MOUSEBUTTONUP:

                # Particle effect on click
                for i in range(80):
                    loc = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
                    p = Particle(loc, (random.randint(0, 20)/10-1, random.randint(0, 20)/10-1), random.randint(1, 4))
                    self.particles.append(p)

                # Button
                mouse_pos = pygame.mouse.get_pos()
                if self.rules_rect.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.rulesUI)
                if self.chat_rect.collidepoint(mouse_pos):
                    self.chatActive = True
                if self.exit_rect.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.menuUI)
                    self.myBoard = Board()
                    self.controller.client.disconnect()
                    self.players[0].score = 0
                    self.players[0].turn = True
                    self.players[1].score = 0
                if self.exit_chat_rect.collidepoint(mouse_pos) and self.chatActive:
                    self.chatActive = False
                #if self.chat_button1_rect.collidepoint(mouse_pos):
                #    self.chatActive = False
                #if self.chat_button2_rect.collidepoint(mouse_pos):
                #    self.chatActive = False
                #if self.chat_button3_rect.collidepoint(mouse_pos):
                #    ...

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
        # Layout helper variables
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Buttons
        self.rules_rect.bottomright = (sw-10, sh-20)
        self.chat_rect.bottomleft = (10, sh-20)
        self.chat_button1_rect.bottomleft = (100, sh - 8)
        self.chat_button2_rect.bottomleft = (250, sh - 8)
        self.chat_button3_rect.bottomleft = (400, sh - 8)
        self.exit_chat_rect.bottomleft = (50, sh-45)
        self.exit_rect.bottomright = (sw-10, sh-20-self.rules_rect.height-20)

        # Board
        self.board_lines_rect.center = (sw / 2 + 5, sh / 2)
        self.board_walls_rect.center = (sw / 2 + 5, sh / 2)
        self.x_offset = sw/2 - ((self.myBoard.width-1)/2)*self.board_distance # offset to center the board
        self.y_offset = sh/2 - ((self.myBoard.height-1)/2)*self.board_distance # offset to center the board

        # Banners
        self.waiting_rect.center = (sw/2, sh/2)
        self.player1_banner_rect.topleft = (0, 0)
        self.player2_banner_rect.topright = (sw, 0)

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
                    self.myBoard = Board()

        # Particles
        self.particles = [particle for particle in self.particles if particle.time > 0]
        for particle in self.particles:
            particle.tick()

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Draw lines of the board
        self.screen.blit(self.boardImg, self.board_lines_rect)

        # Draw connections
        for connection in self.myBoard.connections:
            connection.draw(self.screen, (self.x_offset, self.y_offset))

        # Draw board points
        for row in self.myBoard.points:
            for point in row:
                if not point.is_ball:
                    point.draw(self.screen, pygame.mouse.get_pos(), False, (self.x_offset, self.y_offset))

        # Draw background (board walls)
        self.screen.blit(self.boardWalls, self.board_walls_rect)

        # Draw ball
        for row in self.myBoard.points:
            for point in row:
                if point.is_ball:
                    point.draw(self.screen, pygame.mouse.get_pos(), self.players[0].turn, (self.x_offset, self.y_offset))

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
        # Draw Player Banner
        self.screen.blit(self.player1_banner, self.player1_banner_rect)
        self.screen.blit(self.player2_banner, self.player2_banner_rect)

        # Particles
        for p in self.particles:
            p.draw(self.screen)

        # Waiting banner
        if self.controller.client.current_population == 1:
            self.screen.blit(self.waitingPlayer, self.waiting_rect)
        # Rules icon
        self.screen.blit(self.rules_icon, self.rules_rect)

        # Chat icon
        self.screen.blit(self.chat_icon, self.chat_rect)

        # Exit
        self.screen.blit(self.exit_icon, self.exit_rect)

        # Chat buttons
        if self.chatActive:
            self.screen.blit(self.chat1, self.chat_button1_rect)
            self.screen.blit(self.chat2, self.chat_button2_rect)
            self.screen.blit(self.chat3, self.chat_button3_rect)
            self.screen.blit(self.exit_chat, self.exit_chat_rect)

        # Button select highlights
        mouse_pos = pygame.mouse.get_pos()
        if self.exit_rect.collidepoint(mouse_pos):
            self.screen.blit(self.exit_selected, (self.exit_rect.x, self.exit_rect.y))
        if self.rules_rect.collidepoint(mouse_pos):
            self.screen.blit(self.rules_selected, (self.rules_rect.x, self.rules_rect.y))
        if self.chat_rect.collidepoint(mouse_pos) and not self.chatActive:
            self.screen.blit(self.chat_selected, (self.chat_rect.x, self.chat_rect.y))
        if self.chat_button1_rect.collidepoint(mouse_pos) and self.chatActive:
            self.screen.blit(self.chat1Selected, (self.chat_button1_rect.x, self.chat_button1_rect.y))
        if self.chat_button2_rect.collidepoint(mouse_pos) and self.chatActive:
            self.screen.blit(self.chat2Selected, (self.chat_button2_rect.x, self.chat_button2_rect.y))
        if self.chat_button3_rect.collidepoint(mouse_pos) and self.chatActive:
            self.screen.blit(self.chat3Selected, (self.chat_button3_rect.x, self.chat_button3_rect.y))

        # Show new frame
        pygame.display.flip()

