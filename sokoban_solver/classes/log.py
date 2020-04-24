from aNode import Node

import sys
import time

""" 
This class is used to show reports
"""

class Log:

    """ Constructor """
    def __init__(self):
        self.maxDepth = -1
        self.maxWidth = -1
        self.exploredNodes = 0
        self.startTime = 0
        self.finishTime = 0

    """ Take the initial time """
    def startTiming(self):
        self.startTime = time.time()

    """ Take the final time """
    def finishTiming(self):
        self.finishTime = time.time()

    """ Show a report on the screen. """
    def showReport(self):
        print("Information about the current searching attempt:")
        print("> Maximum reached depth: ", self.maxDepth)
        print("> Maximum reached width: ", self.maxWidth)
        print("> Memory cost (in explored nodes): ", self.exploredNodes)
        print("> Execution time (in sec): ", (self.finishTime - self.startTime))

    """ Updates the report to each new state generated """
    def updateData(self, node):
        if node is not None:
            if node.depth > self.maxDepth:
                self.maxDepth = node.depth

            parent = node.parent

            if parent is not None:
                width = len(parent.children) 
                if width > self.maxWidth:
                    self.maxWidth = width
        
            self.exploredNodes += 1
