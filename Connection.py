import pygame

class Connection:
    """
    Class representing a connection between two points on the field
    """
    def __init__(self, a, b, is_wall=False):
        self.a = a
        self.b = b
        self.is_wall = is_wall
