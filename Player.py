import pygame

class Player:
    """
    Class containing player details
    """

    def __init__(self, name, color, score=0, turn=False):
        self.name = name
        self.color = color
        self.turn = turn
        self.score = score

        # Player unique sprites
        self.lineHImg = pygame.image.load("Art/pink_neon_hor.png")
        self.lineVImg = pygame.transform.rotate(self.lineHImg, 90)
        self.lineDLImg = pygame.image.load("Art/pink_neon_dia.png")
        self.lineDRImg = pygame.transform.flip(self.lineDLImg, False, True)
        self.__saturate(self.lineHImg, color)
        self.__saturate(self.lineVImg, color)
        self.__saturate(self.lineDLImg, color)
        self.__saturate(self.lineDRImg, color)

    def __saturate(self, image, color):
        # zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)