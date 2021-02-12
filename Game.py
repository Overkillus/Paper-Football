from enum import Enum


class Game:
    """
    Data structure class representing the current game session
    """

    # Connection status
    game_status = Enum('','')

    def __init__(self):
        # Current board
        self.myBoard = self.myBoard()
        # Players array
        self.players = []


