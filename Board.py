import math
import numpy as np
import pygame

from Connection import Connection
from Point import Point
from pygame import mixer


class Board:
    """
    Data structure class representing the current state of the board/field
    """
    def __init__(self, width=13, height=9):
        # Variables
        self.width = width
        self.height = height
        # 2D array representing the board
        self.points = [[Point(w, h) for h in range(height)] for w in range(width)]
        # Places ball
        self.points[width//2][height//2].is_ball = True
        # Set storing connections between points (connection holds pointers to point objects from points)
        self.connections = set()
        # Populates map with default connections
        self.generate_walls()

    def add_connection(self, a, b, player=None):
        """
        Creates a connection between two points A and B and adds it to a local set

        :param a: point object A
        :param b: point object B
        :param player: player that made the connection (None if connection is wall)
        :return: boolean: False if operation failed, True otherwise (or connection already exists)
        """
        # Constructing connections (AB and BA)
        ab = Connection(a, b, False, player)

        # Invalid length check
        if not b.is_legal or not a.is_legal:
            return False
        elif not self.__validate_connection_length(ab):
            print("wrong length")
            return False
        # Connection or mirror connection already exists
        elif self.get_connection(a, b) is not None:
            print("already exists")
            return False
        # Add new connection
        else:
            print("added new")
            self.connections.add(ab)
            a.is_used = True
            b.is_used = True
            return True

    def move(self, b, player):
        """
        Tries to make a move to a selected point

        :param b: point to move to
        :param player: player making a move
        :return: boolean: False if operation failed, True otherwise (or connection already exists)
        """
        a = self.get_ball()
        # Boolean
        result = self.add_connection(a, b, player)
        if result:
            connection_sound = mixer.Sound('Sound/moving_effect.wav')  # Sound by LittleSoundRobotFactory @ FreeSound
            connection_sound.play()
            connection_sound.set_volume(0.1)
            a.is_ball = False
            b.is_ball = True
        else:
            fail_sound = mixer.Sound('Sound/fail.wav')  # Sound by LittleSoundRobotFactory @ FreeSound
            fail_sound.play()
            fail_sound.set_volume(0.2)
        return result

    def remove_connection(self, a, b):
        """
        Removes a connection between A and B point objects, non-directional

        :param a: point A
        :param b: point B
        :return: boolean: False if operation failed, True otherwise
        """
        # Constructing connections (AB and BA)
        ab = self.get_connection(a, b)
        ba = self.get_connection(b, a)

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

    def get_ball(self):
        for w in range(self.width):
            for h in range(self.height):
                if self.points[w][h].is_ball:
                    return self.points[w][h]

    def get_connection(self, a, b):
        for connection in self.connections:
            if (connection.a == a and connection.b == b) or (connection.a == b and connection.b == a):
                return connection
        return None

    def update_point_is_used(self, a):
        """
        Updates point is_used based on current connections

        :param a:
        :return:
        """
        for connection in self.connections:
            if connection.a == a or connection.b == a:
                a.is_used = True
                break
        a.is_used = False

    def set_board_distance(self, distance):
        Point.board_distance = distance
        Connection.board_distance = distance
        Connection.lineHImg = pygame.transform.scale(Connection.lineHImg, (distance+15, Connection.lineHImg.get_height()))
        Connection.lineVImg = pygame.transform.scale(Connection.lineVImg, (Connection.lineVImg.get_width(), distance+15))
        Connection.lineDLImg = pygame.transform.scale(Connection.lineDLImg, (distance+15, distance+15))
        Connection.lineDRImg = pygame.transform.scale(Connection.lineDRImg, (distance+15, distance+15))

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

        # Top and Bottom walls for goals
        top_y = self.height//2 - 1
        bottom_y = self.height//2 + 1
        self.add_connection(self.points[0][top_y], self.points[1][top_y])
        self.add_connection(self.points[0][bottom_y], self.points[1][bottom_y])
        self.add_connection(self.points[self.width-1][top_y], self.points[self.width-2][top_y])
        self.add_connection(self.points[self.width-1][bottom_y], self.points[self.width-2][bottom_y])

        # Illegal points
        for i in range(self.height//2 - 1):
            self.points[0][i].is_legal = False
            self.points[0][self.height-1-i].is_legal = False
            self.points[self.width-1][i].is_legal = False
            self.points[self.width-1][self.height-i-1].is_legal = False

        # Goal points
        for j in range(self.height//2 - 1, self.height//2 + 2):
            self.points[0][j].is_goal = True
            self.points[self.width-1][j].is_goal = True

    def add_long_connection(self, a, b):
        """
        Creates a straight long connection between two points A(ax, ay) and B(bx, by) by chaining unit connections between them.

        :param ax: x coordinate of point A
        :param ay: y coordinate of point A
        :param bx: x coordinate of point B
        :param by: y coordinate of point B
        :return: False if operation failed, True otherwise
        """
        # Points not in line
        if a.x != b.x and a.y != b.y:
            return False
        # Same points
        elif a.x == b.x and a.y == b.y:
            return False
        else:
            points = []
            a_distance_from_origin = math.sqrt(a.y**2 + a.x**2)
            b_distance_from_origin = math.sqrt(b.y**2 + b.x**2)

            # Ensure a is closest to origin (0,0)
            # if a_distance_from_origin > b_distance_from_origin:
            #     first
            #     a = b
            #     b = temp

            # Starting point
            points.append(a)
            # Points between a and b
            if a.x == b.x:
                difference = b.y - a.y
                if difference == 1:
                    self.add_connection(a, b)
                    return True
                for i in range(1, difference):
                    point = self.points[a.x][a.y + i]
                    points.append(point)
            elif a.y == b.y:
                difference = b.x - a.x
                if difference == 1:
                    self.add_connection(a, b)
                    return True
                for i in range(1, difference):
                    point = self.points[a.x + i][a.y]
                    points.append(point)
            # Ending point
            points.append(b)

            for i in range(len(points) - 1):
                first = points[i]
                second = points[i+1]
                self.add_connection(first, second)
            return True

    def __validate_connection_length(self, connection):
        """
        Checks if connection (A, B) is made between neighboring points

        :param connection: (A, B) where A and B are point objects
        :return: boolean
        """
        a = connection.a
        b = connection.b
        distance = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
        if distance > 1.5 or distance == 0:
            return False
        else:
            return True
