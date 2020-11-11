import math

import numpy as np


class Board:
    def __init__(self, width=12, height=8):
        self.width = width
        self.height = height
        self.points = np.zeros((width, height))
        self.current = (width/2, height/2)
        self.selected = (-1, -1)
        self.connections = set()

    def add_connection(self, ax, ay, bx, by):
        """
        Creates a connection between two points A(ax, ay) and B(bx, by) and adds it to a local set

        :param ax: x coordinate of point A
        :param ay: y coordinate of point A
        :param bx: x coordinate of point B
        :param by: y coordinate of point B
        :return: False if operation failed, True otherwise
        """
        # Invalid arguments check
        if self.__validate_point(ax, ay) or self.__validate_point(bx, by):
            return False
        # Constructing connections (AB and BA)
        a = (ax, ay)
        b = (bx, by)
        ab = (a, b)
        ba = (b, a)
        # Checking for mirror duplicates
        if not (ab in self.connections or ba in self.connections):
            self.connections.add(ab)
        return True

    def remove_connection(self, ax, ay, bx, by):
        """
        Removes a connection between A(ax, ay) and B(bx, by), non-directional

        :param ax: x coordinate of point A
        :param ay: y coordinate of point A
        :param bx: x coordinate of point B
        :param by: y coordinate of point B
        :return: boolean: False if operation failed, True otherwise
        """
        # Invalid arguments check
        if self.__validate_point(ax, ay) or self.__validate_point(bx, by):
            return False
        # Constructing connections (AB and BA)
        a = (ax, ay)
        b = (bx, by)
        ab = (a, b)
        ba = (b, a)

        self.connections.remove(ab)
        self.connections.remove(ba)
        return True

    def __validate_point(self, ax, ay):
        """
        Checks if a point is on the board

        :param ax: x coordinate of point A
        :param ay: y coordinate of point A
        :return: boolean
        """
        if self.width < ax or ax < 0 or self.height < ay or ay < 0:
            return False
        else:
            return True

    def __validate_connection_length(self, connection):
        """
        Checks if connection (A, B) is made between neighboring points

        :param connection: (A, B) where A and B are points defined by a tuple (x, y)
        :return: boolean
        """
        a = connection[0]
        b = connection[1]
        distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
        if distance > 1.5:
            return False
        else:
            return True
