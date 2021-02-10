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
    chat_icon = pygame.image.load("Art/question_black.png")

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Entity variables
        self.myBoard = Board(13, 9)
        self.board_distance = 50
        self.myBoard.set_board_distance(self.board_distance)
        self.circle_radius = 8
        self.circle_hitbox_multiplier = 1.8
        self.particles = []

        # Buttons
        self.rules_rect = self.rules_icon.get_rect()
        self.chat_rect = self.chat_icon.get_rect()

        # Banners
        self.waiting_rect = self.waitingPlayer.get_rect()

        # Players
        self.players = []
        self.players.append(Player("Player One", Colours.PURPLE))
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

                # Game logic
                for i in range(self.myBoard.width):
                    for j in range(self.myBoard.height):
                        if self.players[0].turn and self.controller.client.current_population == 2:
                            # Square hitbox points in the board
                            hitbox = pygame.Rect(
                                self.board_distance + i * self.board_distance - self.circle_radius * self.circle_hitbox_multiplier,  # X
                                self.board_distance + j * self.board_distance - self.circle_radius * self.circle_hitbox_multiplier,  # Y
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

        # Banners
        self.waiting_rect.center = (sw/2, sh/2)

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
                    for p in self.players:
                        if p.turn:
                            p.score += 1
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
        self.screen.blit(self.boardImg, (0, 0))
        # Draw connections
        for connection in self.myBoard.connections:
            connection.draw(self.screen)

        # Draw board points
        for row in self.myBoard.points:
            for point in row:
                if not point.is_ball:
                    point.draw(self.screen, pygame.mouse.get_pos())

        # Draw Scores
        font = pygame.font.Font(None, 60)
        score1 = font.render(str(self.players[0].score), True, Colours.PURPLE)
        self.screen.blit(score1, (35, 70))
        score2 = font.render(str(self.players[1].score), True, Colours.YELLOW)
        self.screen.blit(score2, (640, 70))

        # Draw background (board walls)
        self.screen.blit(self.boardWalls, (0, 0))

        # Draw ball
        for row in self.myBoard.points:
            for point in row:
                if point.is_ball:
                    point.draw(self.screen, pygame.mouse.get_pos(), self.players[0].turn)

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

        # Show new frame
        pygame.display.flip()

