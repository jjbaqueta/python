import os

""" 
This class implements the game matrix 
"""

class Maze:

    """ Loads a game layout (game matrix) from a file.
        @param fileName: input file's name.
        @param level: level of game.
        @return a loaded map, if the level exists, otherwise, returns an empty map.
    """
    def __init__(self, fileName, level):
        self.numberOfRows = 0
        self.numberOfColumns = 0
    
        if not os.path.exists(fileName):
            raise RuntimeError ("It was not possible to load the game, the levels file does not exist")
        else:
            rowList = []

            file = open(fileName, 'r')
            loading = False        

            for line in file:
                if line.strip() == "$Level " + str(level):
                    loading = False
             
                if loading:
                    content = line.strip()

                    if len(content) > self.numberOfColumns:
                        self.numberOfColumns = len(content)
    
                    rowList.append(content)                    
                    self.numberOfRows += 1

                if line.strip() == "Level " + str(level):
                    loading = True

            file.close()
            self.matrix = [[0 for j in range(self.numberOfColumns)] for i in range(self.numberOfRows)]

            for i, row in enumerate(rowList):
                for j, cell in enumerate(row):
                    self.matrix[i][j] = cell

    """ Checks if a given element is a valid character.
        @param element: a char variable
        @return True, if the element is valid, otherwise, return false.
    """
    def isValidElement(self, element):
        if (element == ' ' or   # Floor
            element == '#' or   # Wall
            element == '@' or   # Player on floor
            element == '.' or   # Dock
            element == '*' or   # Box on dock
            element == '$' or   # Dox
            element == '+' ):   # Player on dock
            return True
        else:
            return False
    
    """ Sets the content of a given position <tuple(row, column)>.
        @param i: row of the game matrix.
        @param j: column of the game matrix.
        @param content: value that will be set on the position(i, j).
    """
    def setContent(self, i, j, content):
        if self.isValidElement(content):
            self.matrix[i][j] = content
        else: print ("ERROR: '" + content + "' is not a valid caractere")

    """ Searches for specific elements on the game matrix
        @param elements: list of the elements to be found.
        @return a list composed of the positions of elements found, otherwise, returns None.
    """
    def __findElements(self, elements):
        elementList = []

        for element in elements:
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):        
                    if self.matrix[i][j] == element:
                        elementList.append((i, j))
        
        if len(elementList) > 0:
            return elementList
        return None

    """ Returns a list composed of the positions of the boxes """
    def findBoxesPos(self):
        boxesPositions = self.__findElements(['$', '*'])
    
        if boxesPositions is None:
            raise RuntimeError ("The maze is not complete, failure to load the boxes")

        return boxesPositions

    """ Returns the player's position """
    def findPlayerPos(self):
        playerPosition = self.__findElements(['@', '+'])[0]

        if playerPosition is None:
            raise RuntimeError ("The maze is not complete, failure to load the player")
        
        return playerPosition

    """ Returns a list composed of the positions of the docks """
    def findDocksPos(self):
        docksPositions = self.__findElements(['.', '+', '*'])

        if docksPositions is None:
            raise RuntimeError ("The maze is not complete, failure to load the docks")
        
        return docksPositions