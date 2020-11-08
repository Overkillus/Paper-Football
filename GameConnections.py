import sys
import pygame
import numpy as np

# Init
from Board import Board

pygame.init()

# Screen variables
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Delta time variables
clock = pygame.time.Clock()
max_tps = 60.0
delta_time = 0

# Entity variables
board_rows = 10
board_columns = 6
board_distance = 50
board = np.zeros((board_rows, board_columns))
myBoard = Board(board_rows, board_columns)

circle_radius = 8
circle_hitbox_multiplier = 1.8


def main():
    global delta_time
    while True:
        event_handler()

        # Ticking
        delta_time += clock.tick()/1000.0
        while delta_time > 1/max_tps:
            delta_time -= 1/max_tps
            update()
        render()


def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.type == pygame.K_q:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONUP:
            for i in range(board_rows):
                for j in range(board_columns):
                    # Square hitbox points in the board
                    hitbox = pygame.Rect(
                        board_distance + i * board_distance - circle_radius * circle_hitbox_multiplier,  # X
                        board_distance + j * board_distance - circle_radius * circle_hitbox_multiplier,  # Y
                        circle_radius * circle_hitbox_multiplier * 2,  # width
                        circle_radius * circle_hitbox_multiplier * 2  # height
                    )
                    if board[i][j] == 1:
                        board[i][j] = 0
                    if hitbox.collidepoint(pygame.mouse.get_pos()):
                        board[i][j] = 1


def update():
    max_tps


def render():
    screen.fill((0, 0, 0))
    for i in range(board_rows):
        for j in range(board_columns):
            if board[i][j] == 0:
                pygame.draw.circle(screen, (255, 255, 255), (50+i*50, 50+j*50), circle_radius, circle_radius)
            else:
                pygame.draw.circle(screen, (255, 20, 20), (50+i*50, 50+j*50), circle_radius, circle_radius)
    pygame.display.flip()


main()
