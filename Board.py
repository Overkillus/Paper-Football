import numpy as np


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = np.zeros((width, height))
        self.selected = (-1, -1)
        self.connections = set()

    def add_connection(self, ax, ay, bx, by):
        if self.__validate_point(ax, ay) or self.__validate_point(bx, by):
            return False
        a = (ax, ay)
        b = (bx, by)
        ab = (a, b)
        ba = (b, a)
        if not (ab in self.connections or ba in self.connections):
            self.connections.add(ab)
        return True

    def remove_connection(self, ax, ay, bx, by):
        if self.__validate_point(ax, ay) or self.__validate_point(bx, by):
            return False
        a = (ax, ay)
        b = (bx, by)
        ab = (a, b)
        ba = (b, a)
        self.connections.remove(ab)
        self.connections.remove(ba)
        return True

    def __validate_point(self, ax, ay):
        if self.width < ax or ax < 0 or self.height < ay or ay < 0:
            return False
        else:
            return True
