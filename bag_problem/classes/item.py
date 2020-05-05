import random
from enums import Constraints

"""
This class implements an item.
"""
class Item:

    """ Constructor: it may generate an item with some fields filled
        @param id: item's identifier
        @param weight: item's weight
        @param value: item's value, importance degree
    """
    def __init__(self, id, weight = None, value = None):
        self.id = id
    
        if weight is None:
            self.weight = random.randint(Constraints.MIN_WEIGHT, Constraints.MAX_WEIGHT)
        else:
            self.weight = weight

        if value is None:
            self.value = random.randint(Constraints.MIN_VALUE, Constraints.MAX_VALUE)
        else:
            self.value = value

    """ Comparator """
    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    """ To string """
    def __str__(self):
        return "id: " + str(self.id) + ", weight: " + str(self.weight) + ", value: " + str(self.value)
