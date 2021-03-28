import math

import pygame

import Settings


class Connection:
    """
    Class representing a connection between two points on the field
    """
    board_distance = 50 # default value, changed later on
    lineHImg = pygame.image.load("Art/Neon/white_neon_hor.png")
    lineVImg = pygame.transform.rotate(lineHImg, 90)
    lineDLImg = pygame.image.load("Art/Neon/white_neon_dia.png")
    lineDRImg = pygame.transform.flip(lineDLImg, False, True)

    def __init__(self, a, b, is_wall=False, player=None):
        self.a = a
        self.b = b
        self.is_wall = is_wall
        self.player = player

    def draw(self, screen, offset=(0, 0)):
        # Omit drawing non player lines
        if self.player is not None:
            # Importing player unique sprites
            lineHImg = self.player.lineHImg
            lineVImg = self.player.lineVImg
            lineDLImg = self.player.lineDLImg
            lineDRImg = self.player.lineDRImg
        else:
            lineHImg = self.lineHImg
            lineVImg = self.lineVImg
            lineDLImg = self.lineDLImg
            lineDRImg = self.lineDRImg

        a = self.a
        b = self.b
        x_difference = b.x - a.x
        y_difference = b.y - a.y
        difference = (x_difference, y_difference)

        # Starting bottom right corner and going clockwise
        if difference == (1, 1):  # Bottom right
            screen.blit(lineDLImg,
                        (offset[0] + self.a.x * self.board_distance - 7,
                         offset[1] + self.a.y * self.board_distance - lineHImg.get_height()/2)
                        )
        elif difference == (0, 1):  # Bottom center
            screen.blit(lineVImg,
                        (offset[0] + self.a.x * self.board_distance - lineVImg.get_width()/2,
                         offset[1] + self.a.y * self.board_distance - 7)
                        )
        elif difference == (-1, 1):  # Bottom left
            screen.blit(lineDRImg,
                        (offset[0] + (self.a.x-1) * self.board_distance - 7,
                         offset[1] + self.a.y * self.board_distance - 7)
                        )
        elif difference == (-1, 0):  # Left center
            screen.blit(lineHImg,
                        (offset[0] + self.b.x * self.board_distance - 7,
                         offset[1] + self.b.y * self.board_distance - lineHImg.get_height()/2)
                        )
        elif difference == (-1, -1):  # Top left
            screen.blit(lineDLImg,
                        (offset[0] + self.b.x * self.board_distance - 7,
                         offset[1] + self.b.y * self.board_distance - lineHImg.get_height() / 2)
                        )
        elif difference == (0, -1):  # Top center
            screen.blit(lineVImg,
                        (offset[0] + self.b.x * self.board_distance - lineVImg.get_width()/2,
                         offset[1] + self.b.y * self.board_distance - 7)
                        )
        elif difference == (1, -1):  # Top right
            screen.blit(lineDRImg,
                        (offset[0] + (self.b.x-1) * self.board_distance - 7,
                         offset[1] + self.b.y * self.board_distance - 7)
                        )
        elif difference == (1, 0):  # Right center
            screen.blit(lineHImg,
                        (offset[0] + self.a.x * self.board_distance - 7,
                         offset[1] + self.a.y * self.board_distance - lineHImg.get_height()/2)
                        )

    def __saturate(self, image, color):
        # zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)