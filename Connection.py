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

    def __init__(self, a, b, is_wall=False):
        self.a = a
        self.b = b
        self.is_wall = is_wall

    def draw(self, screen):
        lineHImg = self.lineHImg.convert_alpha()
        lineVImg = self.lineVImg.convert_alpha()
        lineDLImg = self.lineDLImg.convert_alpha()
        lineDRImg = self.lineDRImg.convert_alpha()

        a = self.a
        b = self.b
        x_difference = b.x - a.x
        y_difference = b.y - a.y
        difference = (x_difference, y_difference)

        # Starting bottom right corner and going clockwise
        if difference == (1, 1):
            screen.blit(lineDLImg,
                        (self.board_distance + self.a.x * self.board_distance - lineHImg.get_width()/10,
                         self.board_distance + self.a.y * self.board_distance - lineHImg.get_height()/2)
                        )
        elif difference == (0, 1):
            screen.blit(lineVImg,
                        (self.board_distance + self.a.x * self.board_distance - lineVImg.get_width()/2,
                         self.board_distance + self.a.y * self.board_distance - lineVImg.get_height()/10)
                        )
        elif difference == (-1, 1):
            screen.blit(lineDRImg,
                        (self.board_distance + (self.a.x-1) * self.board_distance - lineDRImg.get_width()/10,
                         self.board_distance + self.a.y * self.board_distance - lineDRImg.get_height()/10)
                        )
        elif difference == (-1, 0):
            screen.blit(lineHImg,
                        (self.board_distance + self.b.x * self.board_distance - lineHImg.get_width()/10,
                         self.board_distance + self.b.y * self.board_distance - lineHImg.get_height()/2)
                        )
        elif difference == (-1, -1):
            screen.blit(lineDLImg,
                        (self.board_distance + self.b.x * self.board_distance - lineHImg.get_width() / 10,
                         self.board_distance + self.b.y * self.board_distance - lineHImg.get_height() / 2)
                        )
        elif difference == (0, -1):
            screen.blit(lineVImg,
                        (self.board_distance + self.b.x * self.board_distance - lineVImg.get_width()/2,
                         self.board_distance + self.b.y * self.board_distance - lineVImg.get_height()/10)
                        )
        elif difference == (1, -1):
            screen.blit(lineDRImg,
                        (self.board_distance + (self.b.x-1) * self.board_distance - lineDRImg.get_width()/10,
                         self.board_distance + self.b.y * self.board_distance - lineDRImg.get_height()/10)
                        )
        elif difference == (1, 0):
            screen.blit(lineHImg,
                        (self.board_distance + self.a.x * self.board_distance - lineHImg.get_width()/10,
                         self.board_distance + self.a.y * self.board_distance - lineHImg.get_height()/2)
                        )

    # @staticmethod
    # def __validate_connection_length(a, b):
    #     """
    #     Checks if connection (A, B) is made between neighboring points
    #
    #     :return: boolean
    #     """
    #     distance = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    #     if distance > 1.5 or distance == 0:
    #         return False
    #     else:
    #         return True
