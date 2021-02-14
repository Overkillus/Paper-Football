import pygame

from Connection import Connection


class Player:
    """
    Class containing player details
    """

    def __init__(self, name, color, score=0, turn=False):
        self.name = name
        self.__color = color
        self.turn = turn
        self.score = score

        # Player unique sprites
        self.lineHImg = Connection.lineHImg.copy()
        self.lineVImg = pygame.transform.rotate(self.lineHImg, 90)
        self.lineDLImg = Connection.lineDLImg.copy()
        self.lineDRImg = pygame.transform.flip(self.lineDLImg, False, True)
        self.set_color(self.__color)

    def __saturate(self, image, color):
        # Zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # Add in new RGB values
        image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    def get_color(self):
        return self.__color

    def set_color(self, color):
        self.__color = color
        self.__saturate(self.lineHImg, color)
        self.__saturate(self.lineVImg, color)
        self.__saturate(self.lineDLImg, color)
        self.__saturate(self.lineDRImg, color)
