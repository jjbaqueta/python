from screenEnum import Screen
import os

""" 
This class implements the game matrix that will be render on the screen
"""

class Maze:

    """ Loads a game layout (game matrix) from a file.
        @param fileName: input file's name.
        @param level: level of game.
        @return a loaded map, if the level exists, otherwise, returns an empty map.
    """
    def __init__(self, fileName, level):
        self.__rows = int(Screen.GRID_HEIGHT / Screen.FRAME_HEIGHT) + 1
        self.__columns = int(Screen.GRID_WIDTH / Screen.FRAME_WIDTH)
        self.__matrix = [[0 for x in range(self.__columns)] for y in range(self.__rows)] 
        
        for i in range(self.__rows):
            for j in range(self.__columns):
                self.__matrix[i][j] = '#'

        rowList = []
        maxRow = 0
        countColumn = 0
        
        if not os.path.exists(fileName):
            raise RuntimeError ("It was not possible to load the game, the levels file does not exist")
        else:
            file = open(fileName, 'r')            
            loading = False            

            for line in file:
                if line.strip() == "$Level " + str(level):
                    loading = False
                
                if loading:
                    rowList.append(line.strip())
                    
                    if len(rowList) > maxRow:
                        maxRow = len(rowList)
                    
                    countColumn += 1

                if line.strip() == "Level " + str(level):
                    loading = True
        file.close()
        
        if (maxRow > self.__rows or countColumn > self.__columns):
            raise RuntimeError ("It was not possible to load the game, game map does not fit within the screen")
        else:
            x = int((self.__columns / 2) - (countColumn / 2))
            y = int((self.__rows / 2) - (maxRow / 2))
            
            for row in rowList:
                for cell in row:
                    self.__matrix[y][x] = cell
                    x = x + 1
                y = y + 1
                x = int((self.__columns / 2) - (countColumn / 2))
            
    """ Check if the maze is empty.
        @return the size of game matrix, it may returns 0 if the matrix was not initialized.
    """
    def isInitialized(self):
        return len(self.__matrix)

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

    """ Calculates the matrix's size.
        @return the number of frames used to draw the matrix on screen.
    """
    def gridSize(self):
        x = 0
        y = len(self.__matrix)

        for row in self.__matrix:
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)

    """ Get the content stored on the matrix's position(x, y).
        @param x: row of the matrix.
        @param y: column of the matrix.
        @return the content of the position(x, y).
    """
    def getContent(self, x, y):
        return self.__matrix[y][x]
    
    """ Returns the number of rows of the game matrix. """
    def getRows(self):
        return self.__rows
    
    """ Returns the number of columns of the game matrix. """
    def getColumns(self):
        return self.__columns

    """ Returns the game matrix. """
    def getMatrix(self):
        return self.__matrix

    """ Set the content of a given position.
        @param x: row of the matrix.
        @param y: column of the matrix.
        @param content: value that will be set on the position(x, y).
    """
    def setContent(self, x, y, content):
        if self.isValidElement(content):
            self.__matrix[y][x] = content
        else:
            print ("ERROR: Value '" + content + "' to be added is not valid")

    """ Show the game matrix in text mode. """
    def printMatrix(self):
        for row in self.__matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')
