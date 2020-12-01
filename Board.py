import math
import numpy as np
from Point import Point


class Board:
    """
    Data structure class representing the current state of the board/field
    """
    def __init__(self, width=13, height=9):
        self.width = width
        self.height = height
        # 2D array representing the board
        self.points = np.zeros((width, height))
        for w in range(width):
            for h in range(height):
                self.points[w][h] = Point(w, h)

        self.points[width//2][height//2].is_ball = True

        self.connections = set()
        self.generate_walls()

    def add_connection(self, a, b):
        """
        Creates a connection between two points A and B and adds it to a local set

        :param a: point object A
        :param b: point object B
        :return: boolean: False if operation failed, True otherwise (or connection already exists)
        """
        # Constructing connections (AB and BA)
        ab = (a, b)
        ba = (b, a)

        # Invalid length check
        if not self.__validate_connection_length(ab):
            print("wrong length")
            return False
        # Connection or mirror connection already exists
        elif ab in self.connections or ba in self.connections:
            print("already exists")
            return False
        # Add new connection
        else:
            print("added new")
            self.connections.add(ab)
            a.is_used = True
            b.is_used = True
            return True

    def move(self, b):
        """
        Tries to make a move to a selected point

        :param b: point to move to
        :return: boolean: False if operation failed, True otherwise (or connection already exists)
        """
        a = self.current
        return self.add_connection(a, b)

    def remove_connection(self, a, b):
        """
        Removes a connection between A and B point objects, non-directional

        :param a: point A
        :param b: point B
        :return: boolean: False if operation failed, True otherwise
        """
        # Constructing connections (AB and BA)
        ab = (a, b)
        ba = (b, a)

        if ab in self.connections:
            self.connections.remove(ab)
            self.update_point_is_used(a)
            self.update_point_is_used(b)
            return True
        elif ba in self.connections:
            self.connections.remove(ba)
            self.update_point_is_used(a)
            self.update_point_is_used(b)
            return True
        else:
            return False

    def update_point_is_used(self, a):
        """
        Updates point is_used based on current connections

        :param a:
        :return:
        """
        for connection in self.connections:
            if connection[0] == a or connection[1] == a:
                a.is_used = True
                break
        a.is_used = False

    def generate_walls(self):
        # Top and bottom wall
        a = self.points[1][0]
        b = self.points[self.width-2][0]
        self.add_long_connection(a, b)
        a = self.points[1][self.height-1]
        b = self.points[self.width-2][self.height-1]
        self.add_long_connection(a, b)

        # Left and right wall
        a = self.points[1][0]
        b = self.points[1][self.height-1]
        self.add_long_connection(a, b)
        a = self.points[self.width-2][0]
        b = self.points[self.width-2][self.height-1]
        self.add_long_connection(a, b)

        # Adding goals
        for i in range(2):
            for j in range(2):
                ax = 1 + j*(self.width-3)
                ay = self.height//2 - 1 + i
                bx = 1 + j*(self.width-3)
                by = self.height//2 + i
                a = self.points[ax][ay]
                b = self.points[bx][by]
                # print(ax, ay, bx, by)
                self.remove_connection(a, b)

                ax = j*2 + j*(self.width-3)
                ay = self.height//2 - 1 + i
                bx = j*2 + j*(self.width-3)
                by = self.height//2 + i
                a = self.points[ax][ay]
                b = self.points[bx][by]
                # print(ax, ay, bx, by)
                self.add_connection(a, b)

                ax = j*2 + j*(self.width-3)
                ay = self.height//2 - 1 + i
                bx = j*2 + j*(self.width-3)
                by = self.height//2 + i
                a = self.points[ax][ay]
                b = self.points[bx][by]
                # print(ax, ay, bx, by)
                self.add_connection(a, b)

    def add_long_connection(self, ax, ay, bx, by):
        """
        Creates a straight long connection between two points A(ax, ay) and B(bx, by) by chaining unit connections between them.

        :param ax: x coordinate of point A
        :param ay: y coordinate of point A
        :param bx: x coordinate of point B
        :param by: y coordinate of point B
        :return: False if operation failed, True otherwise
        """
        # Points not in line
        if ax != bx and ay != by:
            return False
        # Same points
        elif ax == bx and ay == by:
            return False
        else:
            a = (ax, ay)
            b = (bx, by)
            points = []
            a_distance_from_origin = math.sqrt(ay**2 + ax**2)
            b_distance_from_origin = math.sqrt(by**2 + bx**2)

            # Ensure a is closest to origin (0,0)
            if a_distance_from_origin > b_distance_from_origin:
                temp = a
                a = b
                b = temp

            # Starting point
            points.append(a)
            # Points between a and b
            if ax == bx:
                difference = by - ay
                if difference == 1:
                    self.add_connection(a[0], a[1], b[0], b[1])
                    return True
                for i in range(1, difference):
                    points.append((ax, ay + i))
            elif ay == by:
                difference = bx - ax
                if difference == 1:
                    self.add_connection(a[0], a[1], b[0], b[1])
                    return True
                for i in range(1, difference):
                    points.append((ax + i, ay))
            # Ending point
            points.append(b)

            for i in range(len(points) - 1):
                first = points[i]
                second = points[i+1]
                self.add_connection(first[0], first[1], second[0], second[1])
            return True

    def __validate_connection_length(self, connection):
        """
        Checks if connection (A, B) is made between neighboring points

        :param connection: (A, B) where A and B are point objects
        :return: boolean
        """
        a = connection[0]
        b = connection[1]
        distance = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
        if distance > 1.5 or distance == 0:
            return False
        else:
            return True
