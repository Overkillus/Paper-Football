import numpy as np


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = np.zeros((width, height))
        self.selected = (-1, -1)
        self.connections = set()

    def add_connection(self, ax, ay, bx, by):
        if not self.__validate(ax, ay, bx, by):
            return False
        a = (ax, ay)
        b = (bx, by)
        ab = (a, b)
        ba = (b, a)
        if not (ab in self.connections or ba in self.connections):
            self.connections.add(ab)
        return True

    def remove_connection(self, ax, ay, bx, by):
        if self.__validate(ax, ay, bx, by):
            return False
        a = (ax, ay)
        b = (bx, by)
        ab = (a, b)
        ba = (b, a)
        self.connections.remove(ab)
        self.connections.remove(ba)
        return True

    def __validate(self, ax, ay, bx, by):
        if (self.width < ax or ax < 0 or
                self.width < bx or bx < 0 or
                self.height < ay or ay < 0 or
                self.height < by or by < 0):
            return False
        else:
            return True
