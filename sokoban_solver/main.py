#!../bin/python

import sys
sys.path.append('classes')

from maze import Maze
from pathfinder import Astar
from enums import *
from state import State

"""
This class solves the Sokoban using A* algorithm.
The A* can be configured to execute the following searches:
-> Uniform search (NO_HEURISCT)
-> Informed search (PYTHAGOREAN)
-> Greedy search (GREEDY)
"""
    
def main():
    try:
        # Loading a game layout from the input file 'levels.txt'
        maze = Maze("levels", 1)

        # Finding the player's position
        playerPos = maze.findPlayerPos()

        # Finding the boxes' positions
        boxesPos = maze.findBoxesPos()

        # Finding the docks' positions
        docksPos = maze.findDocksPos()

        # Select the type of search
#        searchType = SearchType.NO_HEURISTIC
#        searchType = SearchType.PYTHAGOREAN
        searchType = SearchType.GREEDY

        # Running the A* algorithm
        solution = Astar.run(maze, State(playerPos, boxesPos), docksPos, searchType)

        if solution is None:
            print("It wasn't found a solution for the current instance of the problem.")
        else:
            print("Depth of the best solution: ", len(solution) - 1)
            print("The best solution is: [output format: Step (Player Pos) {Boxes(id: Pos)} Action]")

            for i, step in enumerate(solution):
                print(i, step.state.playerPos, step.state.boxesPos, step.action)

    except RuntimeError as error: 
        print('Caught this error: ' + repr(error))
        raise 
    except Exception as excp:
        print('Caught this exception: ' + repr(excp))
        raise 

if __name__ == '__main__':
    main()