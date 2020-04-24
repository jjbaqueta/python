""" 
This class implements a game state.
A game state is defined by the player position and the boxes positions.
"""

class State:

    """ @param playerPos: the player's position
        @param boxesPos: a list composed of the positions of the boxes
    """
    def __init__(self, playerPos, boxesPos):
        self.playerPos = playerPos        
        self.boxesPos = boxesPos

    """ Comparator """
    def __eq__(self, other):        
        
        if self.playerPos[0] != other.playerPos[0] or self.playerPos[1] != other.playerPos[1]:
            return False

        for boxSelf in self.boxesPos:
            isEquals = False
            for boxOther in other.boxesPos: 
                if boxSelf[0] == boxOther[0] and boxSelf[1] == boxOther[1]:
                    isEquals = True
                    break
                
            if not isEquals: 
                return False    

        return True