import math

import pygame


class Connection:
    """
    Class representing a connection between two points on the field
    """
    board_distance = 50
    lineHImg = pygame.image.load("Art/pink_neon_hor.png")
    lineVImg = pygame.image.load("Art/pink_neon_vert.png")
    lineDLImg = pygame.image.load("Art/pink_neon_dia.png")
    lineDRImg = pygame.transform.flip(lineDLImg, False, True)

    def __init__(self, a, b, is_wall=False, player=None):
        self.a = a
        self.b = b
        self.is_wall = is_wall
        self.player = player

    def draw(self, screen):

        lineHImg = self.lineHImg.convert_alpha()
        lineVImg = self.lineVImg.convert_alpha()
        lineDLImg = self.lineDLImg.convert_alpha()
        lineDRImg = self.lineDRImg.convert_alpha()
        if self.player is not None:
            color = self.player.color
            self.__saturate(lineHImg, color)
            self.__saturate(lineVImg, color)
            self.__saturate(lineDLImg, color)
            self.__saturate(lineDRImg, color)

        a = self.a
        b = self.b
        x_difference = b.x - a.x
        y_difference = b.y - a.y
        difference = (x_difference, y_difference)

        # Starting bottom right corner and going clockwise
        if difference == (1, 1):  # Bottom right
            screen.blit(lineDLImg,
                        (self.board_distance + self.a.x * self.board_distance - lineHImg.get_width()/10,
                         self.board_distance + self.a.y * self.board_distance - lineHImg.get_height()/2)
                        )
        elif difference == (0, 1):  # Bottom center
            screen.blit(lineVImg,
                        (self.board_distance + self.a.x * self.board_distance - lineVImg.get_width()/2,
                         self.board_distance + self.a.y * self.board_distance - lineVImg.get_height()/10)
                        )
        elif difference == (-1, 1):  # Bottom left
            screen.blit(lineDRImg,
                        (self.board_distance + (self.a.x-1) * self.board_distance - lineDRImg.get_width()/10,
                         self.board_distance + self.a.y * self.board_distance - lineDRImg.get_height()/10)
                        )
        elif difference == (-1, 0):  # Left center
            screen.blit(lineHImg,
                        (self.board_distance + self.b.x * self.board_distance - lineHImg.get_width()/10,
                         self.board_distance + self.b.y * self.board_distance - lineHImg.get_height()/2)
                        )
        elif difference == (-1, -1):  # Top left
            screen.blit(lineDLImg,
                        (self.board_distance + self.b.x * self.board_distance - lineHImg.get_width() / 10,
                         self.board_distance + self.b.y * self.board_distance - lineHImg.get_height() / 2)
                        )
        elif difference == (0, -1):  # Top center
            screen.blit(lineVImg,
                        (self.board_distance + self.b.x * self.board_distance - lineVImg.get_width()/2,
                         self.board_distance + self.b.y * self.board_distance - lineVImg.get_height()/10)
                        )
        elif difference == (1, -1):  # Top right
            screen.blit(lineDRImg,
                        (self.board_distance + (self.b.x-1) * self.board_distance - lineDRImg.get_width()/10,
                         self.board_distance + self.b.y * self.board_distance - lineDRImg.get_height()/10)
                        )
        elif difference == (1, 0):  # Right center
            screen.blit(lineHImg,
                        (self.board_distance + self.a.x * self.board_distance - lineHImg.get_width()/10,
                         self.board_distance + self.a.y * self.board_distance - lineHImg.get_height()/2)
                        )

    def __saturate(self, image, color):
        # zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
