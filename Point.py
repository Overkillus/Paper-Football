import pygame


class Point:
    """
    Class representing a single point in the field
    """
    # ball_img = pygame.image.load("Art/ball_green_glow.png").convert_alpha()
    circle_radius = 8
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
            ball_img = pygame.image.load("Art/ball_green_glow.png").convert_alpha()
            screen.blit(ball_img, (self.board_distance + self.x * self.board_distance - ball_img.get_width() / 2,
                                  self.board_distance + self.y * self.board_distance - ball_img.get_height() / 2))
            # pygame.draw.circle(
            #     screen,
            #     (0, 255, 0),
            #     (self.board_distance+i*self.board_distance, self.board_distance+j*self.board_distance),
            #     circle_radius*1.5,
            # )

        elif self.is_selected:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (self.board_distance + self.x * self.board_distance, self.board_distance + self.y * self.board_distance),
                self.circle_radius,
            )
        elif self.is_legal:
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (self.board_distance + self.x * self.board_distance, self.board_distance + self.y * self.board_distance),
                self.circle_radius,
                self.circle_radius
            )

