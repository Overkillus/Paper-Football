import math

import pygame

class Connection:
    """
    Class representing a connection between two points on the field
    """
    def __init__(self, a, b, is_wall=False):
        self.a = a
        self.b = b
        self.is_wall = is_wall

    def __validate_connection_length(self):
        """
        Checks if connection (A, B) is made between neighboring points

        :return: boolean
        """
        a = self.a
        b = self.b
        distance = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
        if distance > 1.5 or distance == 0:
            return False
        else:
            return True
