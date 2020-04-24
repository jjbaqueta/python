from maze import Maze

""" 
This class implements a view used to show the maze on the screen 
"""
class View:

    """ Prints the game matrix on the screen
        @param maze: game matrix that represents the maze
    """
    @classmethod
    def draw(self, maze):
        print("  ", end =" ")
        for i in range(maze.numberOfColumns):
            print(" " + str(i) + "  ", end =" ")
            
        print("")
            
        for i, row in enumerate(maze.matrix):
            print(str(i) + " " + str(row))        

    """ Updates the maze using the current positions of the player and boxes.
        @param playerPos: the player' position.
        @param boxesPos: a list composed of the positions of the boxes.
        @param maze: the game matrix.
    """
    @classmethod
    def updateMaze(self, playerPos, boxesPos, maze):                
        for i in range(maze.numberOfRows):
            for j in range(maze.numberOfColumns):        
                if maze.matrix[i][j] in ['@', '$']:
                    maze.matrix[i][j] = ' '
                    
                elif maze.matrix[i][j] == '*' or maze.matrix[i][j] == '+':
                    maze.matrix[i][j] = '.'
                    
        playerContent = maze.matrix[playerPos[0]][playerPos[1]]
        
        if playerContent == ' ':
            maze.matrix[playerPos[0]][playerPos[1]] = '@'
        elif playerContent == '.':
            maze.matrix[playerPos[0]][playerPos[1]] = '+'

        for boxPos in boxesPos:
            boxContent = maze.matrix[boxPos[0]][boxPos[1]]
        
            if boxContent == ' ':
                maze.matrix[boxPos[0]][boxPos[1]] = '$'                
            elif boxContent == '.':
                maze.matrix[boxPos[0]][boxPos[1]] = '*'