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
boardImg = pygame.image.load("Art/board_and_lines_neon.png").convert_alpha()
ballImg = pygame.image.load("Art/ball_green_glow.png").convert_alpha()
lineHImg = pygame.image.load("Art/pink_neon_hor.png").convert_alpha()
lineVImg = pygame.image.load("Art/pink_neon_vert.png").convert_alpha()
lineDImg = pygame.image.load("Art/pink_neon_dia.png").convert_alpha() # not sure if diagonal is right


circle_radius = 8
circle_hitbox_multiplier = 1.8

player1Score = 0
player2Score = 0

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

# update player scores
if ballImg.x >= 500:
    player1Score += 1
if ballImg.x >= 20:
    player2Score += 1

def update():
    return True


def render():
    # Clear screen
    screen.fill((0, 0, 0))

    # Draw connections
    for connection in myBoard.connections:
        a = connection.a
        b = connection.b
        start = (board_distance + board_distance * a.x, board_distance + board_distance * a.y)
        end = (board_distance + board_distance * b.x, board_distance + board_distance * b.y)
        pygame.draw.line(screen, (200, 200, 200), start, end, 4)
        connection.draw(screen)
       # screen.blit(lineHImg, (start, end,)) # problem with using image instead of line

    # Draw board points
    for i in range(myBoard.width):
        for j in range(myBoard.height):
            point = myBoard.points[i][j]
            point.draw(screen)

    # Draw Scores
    #font = pygame.font.Font()
    #text = font.render(str(player1Score), 0, BLUE)
    #screen.blit(text, (200, 20))
    #text = font.render(str(player2Score), 0, BLUE)
    #screen.blit(text, (400, 20))

    screen.blit(boardImg, (0, 0))
    pygame.display.flip()


main()
