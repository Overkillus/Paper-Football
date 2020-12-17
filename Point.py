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
        self.ball_scale_time = 0

    def draw(self, screen, mouse_pos, pulse=False):

        # Coordinates
        x = self.board_distance + (self.x * self.board_distance)
        y = self.board_distance + (self.y * self.board_distance)

        # Dynamic point scaling
        size_multiplier = 0.7
        dist = math.hypot(x - mouse_pos[0], y - mouse_pos[1])
        max = (Settings.screen_width + Settings.screen_height) / 3
        b = 1
        a = -b / max
        size_multiplier += a*dist + b

        # Ball pulsing
        ball_scale = 0.75 + (math.sin(self.ball_scale_time) / 3)
        if pulse:
            self.ball_scale_time = (self.ball_scale_time + 0.15) % (2*math.pi)

        if self.is_ball:
            surface = (int(self.ball_img.get_width() * ball_scale), int(self.ball_img.get_height() * ball_scale))
            image = pygame.transform.scale(self.ball_img, surface).convert_alpha()
            screen.blit(image,
                        (x - image.get_width() / 2,
                            y - image.get_height() / 2))
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

