from aNode import Node
from enums import Action
from enums import SearchType
from log import Log
from view import View
from state import State

import copy
import sys

"""
This class implements the A* algorithm.
"""

class Astar:

    """ Uses the manhattan distance as heuristic.
        @param finderPos: current position of the finder <tuple(row, column)>.
        @param targetPos: position of the target <tuple(row, column)>.
        @return the manhattan distance.
    """
    @classmethod
    def __manhattan(self, finderPos, targetPos):
        deltaX = abs(finderPos[0] - targetPos[0])
        deltaY = abs(finderPos[1] - targetPos[1])
        return deltaX + deltaY

    """ Uses the pythagorean distance as heuristic.
        @param finderPos: current position of the finder <tuple(row, column)>.
        @param targetPos: position of the target <tuple(row, column)>.
        @return the pythagorean distance.
    """
    @classmethod
    def __pythagorean(self, finderPos, targetPos):
        deltaX = abs(finderPos[0] - targetPos[0])
        deltaY = abs(finderPos[1] - targetPos[1])
        return (deltaX ** 2 + deltaY ** 2) ** 0.5

    """ Compute the heuristic estimation used by the A* algorithm.
        @param playerPos: the current position of the player <tuple(row, column)>.
        @param boxesPos: the current positions of the boxes list<tuple(row, column)>.
        @param docksPos: the current positions of the docks list<tuple(row, column)>.
        @param searchType: type of the search (NO_HEURIST, MANHATTAN, PYTHAGOREAN, or GREEDY).
        @return the estimation value for the function h.
    """
    @classmethod
    def __computeH(self, playerPos, boxesPos, docksPos, searchType):
        playerH = sys.maxsize
        boxH = sys.maxsize

        for boxPos in boxesPos:
            auxP = 0

            if searchType == SearchType.MANHATTAN:
                auxP = self.__manhattan(playerPos, boxPos)
            else:
                auxP = self.__pythagorean(playerPos, boxPos)

            if playerH > auxP:
                playerH = auxP

            for dockPos in boxesPos:
                auxB = 0

                if searchType == SearchType.MANHATTAN:
                    auxB = self.__manhattan(boxPos, dockPos)
                else:
                    auxB = self.__pythagorean(boxPos, dockPos)

                if boxH > auxB:
                    boxH = auxB

        return playerH + boxH
        
    """ This method checks if all boxes are docked
        @param maze: the maze used in the current game
        @param boxesPos: a list compound of the positions of all boxes
        @return True is the state is end game, otherwise, returns False
    """
    @classmethod
    def __isEndState(self, maze, boxesPos):
        for boxPos in boxesPos:
            boxContent = maze.matrix[boxPos[0]][boxPos[1]]
            
            if boxContent != '*':
                return False
        return True

    """ This method makes a search for boxes from a position <tuple(row, column)>
        @param position: expected position of a box
        @param boxesPos: a list compound of the positions of all boxes
        @return the index of the box, if the box is in the list, otherwise, returns None,
    """
    @classmethod
    def __findBoxByPosition(self, position, boxesPos):
        for i, boxPos in enumerate(boxesPos):
            if boxPos[0] == position[0] and boxPos[1] == position[1]:
                return i
        return -1

    """ The A* algorithm.
        @param maze: the maze used in the current game.
        @param startState: the initial state of the game.
        @param docksPos: the positions of docks.
        @return the path for the finder arrives on the target position.
    """
    @classmethod
    def run(self, maze, startState, docksPos, heuristic):
        log = Log()
        log.startTiming()

        # Creates an initial node using the initial state 
        startNode = Node(None, startState, None)

        # Initializes the search frontier
        openList = []
        closedList = []

        # Adds the initial node in the open list
        openList.append(startNode)

        # Loop until the finder finds the end state (target)
        while len(openList) > 0:
            currentNode = openList[0]
            currentIndex = 0

            for i, node in enumerate(openList):    # Finding the node with smallest cost f
                if node.f < currentNode.f:
                    currentNode = node
                    currentIndex = i
            
            openList.pop(currentIndex)              # Removing the node with the smallest cost from the open list
            closedList.append(currentNode)          # Putting the node with the smallest cost in the closed list

            # Getting information about the current state of the game
            playerPos = currentNode.state.playerPos
            boxesPos = currentNode.state.boxesPos
            View.updateMaze(playerPos, boxesPos, maze)
            
#            View.draw(maze)    # Enable this line to see the temporary mazes on the screen

            if self.__isEndState(maze, boxesPos):
                path = []
                auxNode = currentNode

                while auxNode is not None:
                    path.append(auxNode)
                    auxNode = auxNode.parent

                log.finishTiming()
                log.showReport()

                return path[::-1]

            # If the target wasn't find, explore the neighborhood (4-connected)
            for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                newPosition = (playerPos[0] + direction[0], playerPos[1] + direction[1])

                # Validation of obstacles    
                if newPosition[0] < maze.numberOfRows and newPosition[1] < maze.numberOfColumns:
                    content = maze.matrix[newPosition[0]][newPosition[1]]

                    if content in [' ', '.']:
                        newNode = currentNode.addChild(State(newPosition, copy.deepcopy(boxesPos)), Action.getAction(direction, False))
                        log.updateData(newNode)
        
                    elif content in ['*', '$']:
                        nextPosition = (newPosition[0] + direction[0], newPosition[1] + direction[1])
                        nextContent = maze.matrix[nextPosition[0]][nextPosition[1]]

                        if nextContent in [' ', '.']:

                            boxIndex = self.__findBoxByPosition(newPosition, boxesPos)

                            if self.__findBoxByPosition(newPosition, boxesPos) == -1:
                                raise RuntimeError ("failure to find the box on the position:" + str(newPosition)) 
                            
                            newBoxesPos = copy.deepcopy(boxesPos)
                            newBoxesPos[boxIndex] = nextPosition

                            newNode = currentNode.addChild(State(newPosition, newBoxesPos), Action.getAction(direction, True))
                            log.updateData(newNode)

            # Checks if the node has already been visited
            for child in currentNode.children:
                isClosed = False

                for node in closedList:
                    if child == node:
                        isClosed = True
                        break

                if not isClosed:
                    if heuristic == SearchType.NO_HEURISTIC:
                        child.h = 0
                        child.g = currentNode.g + 1

                    elif heuristic == SearchType.MANHATTAN:
                        child.h = self.__computeH(child.state.playerPos, child.state.boxesPos, docksPos, SearchType.MANHATTAN)
                        child.g = currentNode.g + 1

                    elif heuristic == SearchType.PYTHAGOREAN:
                        child.h = self.__computeH(child.state.playerPos, child.state.boxesPos, docksPos, SearchType.PYTHAGOREAN)
                        child.g = currentNode.g + 1

                    elif heuristic == SearchType.GREEDY:
                        child.h = self.__computeH(child.state.playerPos, child.state.boxesPos, docksPos, SearchType.GREEDY)
                        child.g = 0
                    
                    child.f = child.g + child.h
            
                     # If there is a better path until the node, this path has priority
                    isBetter = True

                    for node in openList:
                        if (child == node and child.g > node.g):
                            isBetter = False
                            break

                    if isBetter:
                        openList.append(child)