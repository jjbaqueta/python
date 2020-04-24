from maze import Maze
from element import Element

try: import queue
except ImportError: import Queue as queue

""" 
This class implements the Sokoban game for one player.
This game was developed using the PyGame engine: https://www.pygame.org/
"""
class Game:
    
    """ Constructor.
        @param level: level of game (check the file 'levels.txt' to see the available levels)
    """
    def __init__ (self, level):
        self.__queue = queue.LifoQueue()        #Queue to undo actions
        self.__maze = Maze("levels", level)

        if self.__maze.isInitialized():            
            playerPos = self.__findPlayerPosition()
            
            if playerPos is not None:
                self.__player = Element(playerPos)
                self.__boxes = self.__findBoxesPosition()
                
                if not len(self.__boxes):
                    raise RuntimeError ("It was not possible to load the game, boxes positions were not defined")
            else: raise RuntimeError ("It was not possible to load the game, player's position was not defined")
        else: raise RuntimeError ("It was not possible to load the game, the informed level not exist")
    
    """ Finds the initial position of the player.
        @return the player's position
    """
    def __findPlayerPosition(self):
        x = 0
        y = 0
        
        for row in self.__maze.getMatrix():
            for cell in row:
                if (cell == '@' or cell == '+'):
                    return (x, y)                
                x = x + 1                    
            y = y + 1
            x = 0            
        return None

    """ Finds the inital positions of the boxes.
        @return a list compound of the positions of the boxes.
    """
    def __findBoxesPosition(self):
        x = 0
        y = 0        
        boxes = []
        
        for row in self.__maze.getMatrix():
            for cell in row:
                if (cell == '$' or cell == '*'):
                    boxes.append(Element((x, y)))   
                x = x + 1
            y = y + 1
            x = 0
        return boxes

    """ Checks if the player can be moved.
        @param xOffset: x-axis offset.
        @param yOffset: y-axis offset.
        @return True, if the movement is possible, otherwise, return False.
    """
    def __canMove(self, xOffset, yOffset):
        posX = self.__player.getPosX()
        posY = self.__player.getPosY()

        if self.__maze.getContent(posX + xOffset, posY + yOffset) in ['#','*','$']:
            return False        
        return True

    """ Checks if the player can push a box.
        @param xOffset: x-axis offset.
        @param yOffset: y-axis offset.
        @return True, if the movement is possible, otherwise, return False.
    """
    def __canPush(self, xOffset, yOffset):
        posX = self.__player.getPosX()
        posY = self.__player.getPosY()

        if (self.__maze.getContent(posX + xOffset, posY + yOffset) in ['*','$'] and 
            self.__maze.getContent(posX + (xOffset * 2), posY + (yOffset * 2)) in [' ','.']):
            return True        
        return False

    """ Updates the position of a box.
        @param box: the box that is being pushed.
        @param xOffset: x-axis offset.
        @param yOffset: y-axis offset.
    """
    def updateBoxCoordinates(self, box, xOffset, yOffset):
        newX = box.getPosX() + xOffset
        newY = box.getPosY() + yOffset

        boxContent = self.__maze.getContent(box.getPosX(), box.getPosY())
        newContent = self.__maze.getContent(newX, newY)

        if boxContent == '$' and newContent == ' ':
            self.__maze.setContent(newX, newY, '$')
            self.__maze.setContent(box.getPosX(), box.getPosY(), ' ')

        elif boxContent == '$' and newContent == '.':
            self.__maze.setContent(newX, newY, '*')
            self.__maze.setContent(box.getPosX(), box.getPosY(), ' ')

        elif boxContent == '*' and newContent == ' ':
            self.__maze.setContent(newX, newY, '$')
            self.__maze.setContent(box.getPosX(), box.getPosY(), '.')

        elif boxContent == '*' and newContent == '.':
            self.__maze.setContent(newX, newY, '*')
            self.__maze.setContent(box.getPosX(), box.getPosY(), '.')

        box.updatePosition((newX, newY))

    """ Updates the position of the player.
        @param xOffset: x-axis offset.
        @param yOffset: y-axis offset.
    """
    def updatePlayerCoordinates(self, xOffset, yOffset):

        newPlayerX = self.__player.getPosX() + xOffset
        newPlayerY = self.__player.getPosY() + yOffset

        currentContent = self.__maze.getContent(self.__player.getPosX(), self.__player.getPosY())
        newContent = self.__maze.getContent(newPlayerX, newPlayerY)

        if currentContent == '@' and newContent == ' ':
            self.__maze.setContent(newPlayerX, newPlayerY, '@')
            self.__maze.setContent(self.__player.getPosX(), self.__player.getPosY(), ' ')

        elif currentContent == '@' and newContent == '.':
            self.__maze.setContent(newPlayerX, newPlayerY, '+')
            self.__maze.setContent(self.__player.getPosX(), self.__player.getPosY(), ' ')

        elif currentContent == '+' and newContent == ' ':
            self.__maze.setContent(newPlayerX, newPlayerY, '@')
            self.__maze.setContent(self.__player.getPosX(), self.__player.getPosY(), '.')

        elif currentContent == '+' and newContent == '.':
            self.__maze.setContent(newPlayerX, newPlayerY, '+')
            self.__maze.setContent(self.__player.getPosX(), self.__player.getPosY(), '.')

        self.__player.updatePosition((newPlayerX, newPlayerY))

    """ Moves the player to a new position.
        @param box current box
        @param x-axis offset.
        @param y-axis offset.
    """
    def movePlayer(self, xOffset, yOffset):        
        if self.__canPush(xOffset, yOffset):            
            print("pushing... offset(" + str(xOffset) + "," + str(yOffset) + ")")
            
            boxX = self.__player.getPosX() + xOffset
            boxY = self.__player.getPosY() + yOffset            
            box = self.getBoxByPosition(boxX, boxY)

            if box is not None:
                self.updateBoxCoordinates(box, xOffset, yOffset)
                self.updatePlayerCoordinates(xOffset, yOffset)
                self.__queue.put((xOffset, yOffset, box))                
            else:
                raise RuntimeError ("failure to search for the box (position: " + str(boxX) + ", " + str(boxY) + ")")
    
        if self.__canMove(xOffset, yOffset):            
            print("moving ... offset(" + str(xOffset) + "," + str(yOffset) + ")")            

            self.updatePlayerCoordinates(xOffset, yOffset)
            self.__queue.put((xOffset, yOffset, None))            
            
        print("player(x,y) -> (x',y') : (" + 
              str(self.__player.getPosX() - xOffset) + "," + 
              str(self.__player.getPosY() - yOffset) + ") -> (" +
              str(self.__player.getPosX()) + "," + 
              str(self.__player.getPosY()) + ")")
    
    """ Undo the last movement. """
    def unmove(self):        
        if not self.__queue.empty():
            movement = self.__queue.get()
            
            if movement[2] is None:
                self.updatePlayerCoordinates(movement[0] * -1, movement[1] * -1)
            else:
                box = movement[2]                
                self.updatePlayerCoordinates(movement[0] * -1, movement[1] * -1)
                self.updateBoxCoordinates(box, movement[0] * -1, movement[1] * -1)
                
    """ Returns if is game over. """
    def isEndGame(self):
        for row in self.__maze.getMatrix():
            for cell in row:
                if cell == '$':
                    return False
        return True

    """ Searches for a box by its position.
        @param x: the position of the box on the x-axis.
        @param y: the position of the box on the y-axis
        @return the box, in case of successful, otherwise, return None.
    """
    def getBoxByPosition(self, x, y):
        for box in self.__boxes:
            if box.getPosition()[0] == x and box.getPosition()[1] == y:
                return box
        return None

    """ Returns the game matrix. """
    def getMaze(self):
        return self.__maze

    """ Shows the positions of player and boxes."""
    def showCoordinates(self):
        print("Player: " + str(self.__player.getPosition()))

        for box in self.__boxes:
            print("Box: " + str(box.getPosition()))

    """ Shows the game matrix on the screen. """        
    def showGameBoard(self):
        for row in self.__maze.getMatrix():
            print (row)
