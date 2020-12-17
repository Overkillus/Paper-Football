import math

import pygame

import Settings


class Point:
    """
    Class representing a single point in the field
    """
    circle_radius = 5
    board_distance = 50
    ball_img = pygame.image.load("Art/ball_green_glow.png")

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.is_used = False
        self.is_ball = False
        self.is_goal = False
        self.is_legal = True
        self.is_selected = False

    def draw(self, screen, mouse_pos):

        # Coordinates
        x = self.board_distance + (self.x * self.board_distance)
        y = self.board_distance + (self.y * self.board_distance)

        # Dynamic scaling
        size_multiplier = 0.7
        dist = math.hypot(x - mouse_pos[0], y - mouse_pos[1])
        max = (Settings.screen_width + Settings.screen_height) / 3
        b = 1
        a = -b / max
        size_multiplier += a*dist + b

        if self.is_ball:
            screen.blit(self.ball_img.convert_alpha(),
                        (x - self.ball_img.get_width() / 2,
                        y - self.ball_img.get_height() / 2))
        elif self.is_selected or self.is_goal:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (x, y),
                self.circle_radius * size_multiplier,
            )
        elif self.is_legal:
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (x, y),
                self.circle_radius * size_multiplier,
            )

