from enum import IntEnum

"""
This class implements all enums used in the program.
"""

class SearchType(IntEnum):
    NO_HEURISTIC = 0
    MANHATTAN = 1
    PYTHAGOREAN = 2
    GREEDY = 3

class Action(IntEnum):
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_RIGHT = 3
    MOVE_LEFT = 4

    PUSH_UP = 5
    PUSH_DOWN = 6
    PUSH_RIGHT = 7
    PUSH_LEFT = 8

    """ Checks if the player is pushing a box
        @param action: an action performed by player
        @return True, if the player is pushing a box, otherwise, return False
    """
    @classmethod
    def isPushing(self, action):
        if (action == self.PUSH_UP or 
            action == self.PUSH_DOWN or 
            action == self.PUSH_RIGHT or 
            action == self.PUSH_LEFT):
            return True
        else:
            return False

    """ Translates a push action to a move action
        @param action: an action performed by player
        @return a move action
    """
    @classmethod
    def convertToMove(self, action):
        if action == self.PUSH_UP: return self.MOVE_UP
        elif action == self.PUSH_DOWN: return self.MOVE_DOWN 
        elif action == self.PUSH_RIGHT: return self.MOVE_RIGHT 
        elif action == self.PUSH_LEFT: return self.MOVE_LEFT
        else: None

    """ Translates a move action to a push action
        @param action: an action performed by player
        @return a push action
    """
    @classmethod
    def convertToPush(self, action):
        if action == self.MOVE_UP: return self.PUSH_UP
        elif action == self.MOVE_DOWN: return self.PUSH_DOWN 
        elif action == self.MOVE_RIGHT: return self.PUSH_RIGHT 
        elif action == self.MOVE_LEFT: return self.PUSH_LEFT
        else: None

    """ Returns an action based on a informed direction.
        @param direction: a direction that player has taken <tuple(row, column)>.
        @param hasBox: logic value that defines if there is a box forward
        @return an action.
    """
    @classmethod
    def getAction(self, direction, hasBox):
        if (direction == (0, 1) and hasBox): return self.PUSH_RIGHT
        elif (direction == (0, -1) and hasBox): return self.PUSH_LEFT
        elif (direction == (1, 0) and hasBox): return self.PUSH_DOWN
        elif (direction == (-1, 0) and hasBox): return self.PUSH_UP
        elif (direction == (0, 1) and not hasBox): return self.MOVE_RIGHT
        elif (direction == (0, -1) and not hasBox): return self.MOVE_LEFT
        elif (direction == (1, 0) and not hasBox): return self.MOVE_DOWN
        elif (direction == (-1, 0) and not hasBox): return self.MOVE_UP

    """ Returns a direction based on an action.
        @param action: an action performed by the player.
        @return the direction that will be taken <tuple(row, column)>.
    """
    @classmethod
    def getDirection(self, action):
        if (action == self.MOVE_UP or action == self.PUSH_UP):
            return (-1, 0)
        elif (action == self.MOVE_DOWN or action == self.PUSH_DOWN):
            return (1, 0)
        elif (action == self.MOVE_LEFT or action == self.PUSH_LEFT):
            return (0, -1)
        elif (action == self.MOVE_RIGHT or action == self.PUSH_RIGHT):
            return (0, 1)
    
    """ To string """
    def __str__(self):
        return self.name