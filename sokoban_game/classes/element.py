""" 
This class implements an element.
An element can be instanced as box or player
"""

class Element:
    """ Constructor.
        @param position: the element's position.
    """
    def __init__ (self, position):
        self.__x = position[0]
        self.__y = position[1]

    def setPosXY(self, x, y):
        self.__x = x
        self.__y = y

    def getPosX(self):
        return self.__x

    def getPosY(self):
        return self.__y

    def getPosition(self):
        return (self.__x, self.__y)

    def updatePosition(self, newPosition):
        self.setPosXY(newPosition[0], newPosition[1])
