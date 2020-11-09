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
myBoard = Board(10, 6)
board_distance = 50

circle_radius = 8
circle_hitbox_multiplier = 1.8


def main():
    global delta_time
    myBoard.add_connection(0,0,1,1)
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
            for i in range(myBoard.width):
                for j in range(myBoard.height):
                    # Square hitbox points in the board
                    hitbox = pygame.Rect(
                        board_distance + i * board_distance - circle_radius * circle_hitbox_multiplier,  # X
                        board_distance + j * board_distance - circle_radius * circle_hitbox_multiplier,  # Y
                        circle_radius * circle_hitbox_multiplier * 2,  # width
                        circle_radius * circle_hitbox_multiplier * 2  # height
                    )
                    if hitbox.collidepoint(pygame.mouse.get_pos()):
                        myBoard.add_connection(myBoard.selected[0], myBoard.selected[1], i, j)
                        myBoard.selected = (i, j)


def update():
    max_tps


def render():
    screen.fill((0, 0, 0))
    for i in range(myBoard.width):
        for j in range(myBoard.height):
            if myBoard.selected == (i, j):
                pygame.draw.circle(screen, (255, 0, 0), (50+i*50, 50+j*50), circle_radius, circle_radius)
            else:
                pygame.draw.circle(screen, (255, 255, 255), (50+i*50, 50+j*50), circle_radius, circle_radius)

    for connection in myBoard.connections:
        start = (board_distance + board_distance * connection[0][0], board_distance + board_distance * connection[0][1])
        end = (board_distance + board_distance * connection[1][0], board_distance + board_distance * connection[1][1])
        pygame.draw.line(screen, (200, 200, 200), start, end)

    pygame.display.flip()


main()
