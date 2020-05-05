from item import Item
from enums import Constraints

"""
This class implements the datasets used as input
"""
class Dataset:

    """ This method generates a defaul fixed dataset
        @return a list of items
    """    
    @classmethod
    def generateDefaultDataset(self):
        items = []
        items.append(Item(1, 3, 1))
        items.append(Item(2, 8, 3))
        items.append(Item(3, 12, 1))
        items.append(Item(4, 2, 8))
        items.append(Item(5, 8, 9))
        items.append(Item(6, 4, 3))
        items.append(Item(7, 4, 2))
        items.append(Item(8, 5, 8))
        items.append(Item(9, 1, 5))
        items.append(Item(10, 1, 1))
        items.append(Item(11, 8, 1))
        items.append(Item(12, 6, 6))
        items.append(Item(13, 4, 3))
        items.append(Item(14, 3, 2))
        items.append(Item(15, 3, 5))
        items.append(Item(16, 5, 2))
        items.append(Item(17, 7, 3))
        items.append(Item(18, 3, 8))
        items.append(Item(19, 5, 9))
        items.append(Item(20, 7, 3))
        items.append(Item(21, 4, 2))
        items.append(Item(22, 3, 4))
        items.append(Item(23, 7, 5))
        items.append(Item(24, 2, 4))
        items.append(Item(25, 3, 3))
        items.append(Item(26, 5, 1))
        items.append(Item(27, 4, 3))
        items.append(Item(28, 3, 2))
        items.append(Item(29, 7, 14))
        items.append(Item(30, 19, 32))
        items.append(Item(31, 20, 20))
        items.append(Item(32, 21, 19))
        items.append(Item(33, 11, 15))
        items.append(Item(34, 24, 37))
        items.append(Item(35, 13, 18))
        items.append(Item(36, 17, 13))
        items.append(Item(37, 18, 19))
        items.append(Item(38, 6, 10))
        items.append(Item(39, 15, 15))
        items.append(Item(40, 25, 40))
        items.append(Item(41, 12, 17))
        items.append(Item(42, 19, 39))
    
        return items

    """ This method generates a random dataset
        @return a list of items
    """    
    @classmethod
    def generateRandomDataset(self):
        items = []

        for i in range(1, Constraints.DATASET_SIZE + 1):
            items.append(Item(i))

        return items
            
    """ Show all items of a dataset on the screen 
        @param dataset: the dataset that will be shown
    """
    @classmethod
    def show(self, dataset):
        for item in dataset:
            print(item)
