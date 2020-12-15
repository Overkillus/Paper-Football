import sys
import pygame

# Init
import Colours
import Settings
from Board import Board
from Player import Player


class Game:

    # Art
    boardImg = pygame.image.load("Art/board_lines.png")
    boardWalls = pygame.image.load("Art/board_walls.png")

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
                for i in range(self.myBoard.width):
                    for j in range(self.myBoard.height):
                        if self.players[0].turn:
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

                                # # TODO temp
                                if result:
                                    self.controller.client.send_to_server(("!MOVE", (i, j)))
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
                point.draw(self.screen)

        # Draw Scores
        font = pygame.font.Font(None, 60)
        score1 = font.render(str(self.players[0].score), True, Colours.WHITE)
        self.screen.blit(score1, (35, 70))
        score2 = font.render(str(self.players[1].score), True, Colours.WHITE)
        self.screen.blit(score2, (640, 70))

        # Draw background (board walls)
        self.screen.blit(self.boardWalls, (0, 0))

        # Show new frame
        pygame.display.flip()

