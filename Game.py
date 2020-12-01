import sys
import pygame

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
myBoard = Board(13, 9)
board_distance = 50


circle_radius = 10
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
                        # myBoard.add_connection(myBoard.selected[0], myBoard.selected[1], i, j)
                        point = myBoard.points[i][j]
                        myBoard.move(point)
                        # for point in myBoard.points:
                        #     point.is_selected = False
                        # point.is_selected = True
                        for w in range(myBoard.width):
                            for h in range(myBoard.height):
                                current_point = myBoard.points[w][h]
                                current_point.is_selected = False
                        point.is_selected = True


def update():
    return True


def render():
    # Clear screen
    screen.fill((0, 0, 0))
    # Draw board points
    for i in range(myBoard.width):
        for j in range(myBoard.height):
            point = myBoard.points[i][j]
            if point.is_ball:
                pygame.draw.circle(
                    screen,
                    (0, 255, 0),
                    (board_distance+i*board_distance, board_distance+j*board_distance),
                    circle_radius*1.5,
                )
            elif point.is_selected:
                pygame.draw.circle(
                    screen,
                    (255, 0, 0),
                    (board_distance+i*board_distance, board_distance+j*board_distance),
                    circle_radius,
                )
            elif point.is_legal:
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (board_distance+i*board_distance, board_distance+j*board_distance),
                    circle_radius,
                    circle_radius
                )

    for connection in myBoard.connections:
        a = connection[0]
        b = connection[1]
        start = (board_distance + board_distance * a.x, board_distance + board_distance * a.y)
        end = (board_distance + board_distance * b.x, board_distance + board_distance * b.y)
        pygame.draw.line(screen, (200, 200, 200), start, end, 4)

    pygame.display.flip()


main()
