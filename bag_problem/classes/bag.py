from item import Item

"""
This class implements a bag
"""
class Bag:

    """ Constructor """
    def __init__(self):
        self.amountItems = 0
        self.weight = 0
        self.fitness = 0
        self.items = []

    """ This method maps the items to a bag according to the gene
        @param dataset: list of all possible items 
        @param gene: a binary representation, which represents the items that will be put inside the bag
    """
    def makeMapping(self, dataset, gene):
        for i, allele in enumerate(gene):
            if allele == 1:
                item = dataset[i]
                self.fitness += item.value
                self.weight += item.weight
                self.amountItems += 1
                self.items.append(item)

    """ This method shows a bag on the screen """
    def show(self):
        print("Amount of items: ", self.amountItems)
        print("Bag's weight: ", self.weight)
        print("Bag's fitness: ", self.fitness)
        print("Bag's items:")

        for i, item in enumerate(self.items):
            print(i + 1, item)
