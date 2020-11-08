import numpy as np


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = np.zeros((width, height))
        self.connections = set()

    def add_connection(self, ax, ay, bx, by):
        a = (ax, ay)
        b = (bx, by)
        ab = (a, b)
        ba = (b, a)
        if not (set.__contains__(ab) or set.__contains__(ba)):
            set.add(ab)

    def remove_connection(self, ax, ay, bx, by):
        a = (ax, ay)
        b = (bx, by)
        ab = (a, b)
        ba = (b, a)
        set.remove(ab)
        set.remove(ba)