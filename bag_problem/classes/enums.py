from enum import IntEnum

"""
This file implements all enums used in the program.
"""

class Constraints(IntEnum):
    MIN_WEIGHT = 1
    MAX_WEIGHT = 25
    MIN_VALUE = 1
    MAX_VALUE = 40
    DATASET_SIZE = 42
    BAG_CAPACITY = 120
    NUMBER_OF_MUTATION = 4
    
    """ To string """
    def __str__(self):
        return self.name + str(self.value)

class FitnessType(IntEnum):
    PENALIZING = 1
    REPAIRING = 2
