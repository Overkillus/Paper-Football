

class Point:
    """
    Class representing a single point in the field
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.is_used = False
        self.is_ball = False
        self.is_goal = False
        self.is_legal = True
        self.is_selected = False

