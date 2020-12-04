import pygame


class Point:
    """
    Class representing a single point in the field
    """
    ball_img = pygame.image.load("Art/ball_green_glow.png")
    circle_radius = 6
    board_distance = 50

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.is_used = False
        self.is_ball = False
        self.is_goal = False
        self.is_legal = True
        self.is_selected = False

    def draw(self, screen):
        if self.is_ball:
            screen.blit(self.ball_img.convert_alpha(),
                        (self.board_distance + self.x * self.board_distance - self.ball_img.get_width() / 2,
                        self.board_distance + self.y * self.board_distance - self.ball_img.get_height() / 2))

        elif self.is_selected:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (self.board_distance + self.x * self.board_distance,
                 self.board_distance + self.y * self.board_distance),
                self.circle_radius,
            )
        elif self.is_legal:
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (self.board_distance + self.x * self.board_distance,
                 self.board_distance + self.y * self.board_distance),
                self.circle_radius,
            )

