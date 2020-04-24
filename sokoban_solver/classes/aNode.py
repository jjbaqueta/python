from state import State

""" 
This class implements the node used in the A* pathfinding class 
"""

class Node:

    """ @param parent: parent of current node.
        @param state: the current game state.
        @param action: the last action taken that has generated the current game state
    """
    def __init__(self, parent = None, state = None, action = None):
        self.parent = parent    
        self.state = state   
        self.depth = 0      
        self.children = []
        self.action = action

        self.g = 0      # Accumulated cost
        self.h = 0      # Heuristic cost
        self.f = 0      # Total cost

    """ Creates an association between the father node (self) and a child node.
        @param state: the current game state.
        @param action: the last action taken that has generated the current game state.
        @return a new instance of a Node (son).
    """
    def addChild(self, state, action):
        child = Node(self, state, action)
        child.depth = self.depth + 1
        self.children.append(child)
        return child
            
    """ Comparator """
    def __eq__(self, other):
        return self.state == other.state

    """ To string """
    def __str__(self):
        return "player: " + str(self.state.playerPos) + ", boxes: " + str(self.state.boxesPos)
