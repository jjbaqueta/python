#!../bin/python

import sys
import pygame
import string

sys.path.append('classes')

from game import Game
from screenEnum import Screen
  
""" This file execute the Sokoban game. """

#Constants
WALL = pygame.image.load('images/wall.png')
FLOOR = pygame.image.load('images/floor.png')
BOX = pygame.image.load('images/box.png')
BOX_DOCKED = pygame.image.load('images/box_docked.png')
PLAYER = pygame.image.load('images/player.png')
PLAYER_DOCKED = pygame.image.load('images/player_dock.png')
DOCKER = pygame.image.load('images/dock.png')
BACKGROUND = 0, 0, 0

""" Prints the game matrix on the screen in board mode.
    @param screen: the space to draw the elements of the game.
    @param matrix: the game matrix with all elements of the game.
"""
def printGame(screen, matrix):    
    screen.fill(BACKGROUND)
    x = 0
    y = 0

    for row in matrix:
        for cell in row:
            if cell == ' ': screen.blit(FLOOR,(x, y))
            elif cell == '#': screen.blit(WALL,(x, y))
            elif cell == '@': screen.blit(PLAYER,(x, y))
            elif cell == '.': screen.blit(DOCKER,(x, y))
            elif cell == '*': screen.blit(BOX_DOCKED,(x, y))
            elif cell == '$': screen.blit(BOX,(x, y))
            elif cell == '+': screen.blit(PLAYER_DOCKED,(x,y))
            x = x + 32        
        x = 0
        y = y + 32        

""" Prints a message within a box on the middle of the screen.
    @param screen: the space to draw the elements of the game.
    @param message: information to be shown.
"""
def displayBox(screen, message):    
    fontobject = pygame.font.Font(None,18)
    
    pygame.draw.rect(screen, (0,0,0), 
        ((screen.get_width() / 2) - 125, 
        (screen.get_height() / 2) - 10, 300,20), 0)
    
    pygame.draw.rect(screen, (255,255,255), 
    ((screen.get_width() / 2) - 127,
    (screen.get_height() / 2) - 12, 304,24), 1)
        
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
        ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        pygame.display.flip()

""" Shows the message of end of level,
    @param screen: the space to draw the elements of the game.
"""
def displayEnd(screen):
    message = "Level Completed: press (n) to next level."
    displayBox(screen, message)
    
""" Shows a message about the player's options.
    @param screen: the space to draw the elements of the game.
"""
def displayOptions(screen):   
    fontobject = pygame.font.Font(None,18)        
    screen.blit(fontobject.render("Press: (z) to back the movement, and (q) to exit.", 
                                  1, (255,255,255)),(10, screen.get_height() - 20))

""" Catches the keys pressed by the user.
    @return the key pressed at the moment.
"""
def getKey():
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass

#Starting the game 
def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((Screen.GRID_WIDTH, Screen.GRID_HEIGHT + 30))

        level = 1

        while 1:
            game = Game(level)
            nextLevel = False
            levelEnd = False

            while not nextLevel:            

                if game.isEndGame():
                    levelEnd = True
                    displayEnd(screen)

                printGame(screen, game.getMaze().getMatrix())
                displayOptions(screen)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        sys.exit(0)
                        
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z:
                            levelEnd = False
                            game.unmove()

                        elif event.key == pygame.K_q: 
                            sys.exit(0)

                        elif not levelEnd:                    
                            if event.key == pygame.K_UP: 
                                game.movePlayer(0, -1)
                                
                            elif event.key == pygame.K_DOWN: 
                                game.movePlayer(0, 1)
                                
                            elif event.key == pygame.K_LEFT: 
                                game.movePlayer(-1, 0)
                                
                            elif event.key == pygame.K_RIGHT: 
                                game.movePlayer(1, 0)
                        else:
                            if event.key == pygame.K_n:
                                nextLevel = True
                                level += 1

                                if level > 12:
                                    level = 1                    

                pygame.display.update()
            
    except RuntimeError as error: 
        print('Caught this error: ' + repr(error))
        raise 
    except TypeError as error:
        print('Caught this error: ' + repr(error))
        raise 
    except Exception as excp:
        print('Caught this exception: ' + repr(excp))
        raise 

if __name__ == '__main__':
    main()
