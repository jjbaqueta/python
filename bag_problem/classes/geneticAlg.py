import random
import sys
from enums import *
from dataset import Dataset
from bag import Bag

"""
This class implements a canonical Genetic Algorithm (GA)
"""
class GA:

    """ Constructor """
    def __init__(self):
#        self.items = Dataset.generateRandomDataset()
        self.items = Dataset.generateDefaultDataset()
        self.population = []
        self.bestGeneration = 0
        self.bestFitness = 0
        self.bestGene = None
        self.__generationId = 0

    """ This method generates the initial population for the experiment
        @param populationSize: the population's size
    """    
    def createPopulation(self, populationSize):
        for i in range(populationSize):
            self.population.append(self.__createRandomGene())
        
    """ This method generates a gene from a dataset
        @return a binary list, which represents a bag
    """
    def __createRandomGene(self):
        gene = []

        for i in range(Constraints.DATASET_SIZE):
            gene.append(random.randint(0, 1))
        return gene

    """ This method computes the fitness value for a gene (a possible bag)
        If the bag is too weight, one of the following approaches can be adopted to fix a infactible bag:
        - penalizing: the bag's fitness value is set as 1 or as a normalized value
        - repairing: a given element is removed from the bag and the fitness value is calculated again
        @param gene: a binary representation, which represents the items that will be put inside the bag
        @param typeComputation: a enum value, if PENALIZING, an infactible gene is penalized, otherwise, the gene is repaired
        @return the fitness value of gene
    """
    def __computeFitness(self, gene, typeComputation):
        score = 0
        bagWeight = 0

        for i, allele in enumerate(gene):
            if allele == 1:
                bagWeight += self.items[i].weight
                score += self.items[i].value

        if bagWeight > Constraints.BAG_CAPACITY:
            if typeComputation == FitnessType.PENALIZING:
                penalizingRate = Constraints.BAG_CAPACITY / bagWeight
                if penalizingRate >= 0.95:
                    return score * penalizingRate
                else:
                    return 1
            else:
                worstScore = sys.maxsize
                worstIndex = 0

                for i in range(len(gene)):
                    if gene[i] == 1:
                        score = self.items[i].value

                        if score < worstScore:
                            worstScore = score
                            worstIndex = i

                gene[worstIndex] = 0
                return self.__computeFitness(gene, typeComputation)

        return score

    """ This method selects the individuals that will compound the reproduction group.
        @param numberOfSelected: number of parents for generation
        @param penalizing: a logic value, if True, an infactible gene is penalized, otherwise, the gene is repaired
        @return the selected individuals
    """ 
    def selectParents(self, numberOfSelected, penalizing):
        scores = []
        parents = []
        totalFitness = 0
        self.__generationId += 1

        for gene in self.population:
            fitness = self.__computeFitness(gene, penalizing)
            totalFitness += fitness    
            scores.append(fitness)

            if fitness > self.bestFitness:
                self.bestFitness = fitness
                self.bestGene = gene
                self.bestGeneration = self.__generationId

        for i in range(numberOfSelected):
            parents.append(self.__rouletteWheel(scores, totalFitness))

        return parents
            
    """ This method implements the roulette wheel used to select individuals.
        @param scores: a list with the fitness value of each individual from the population
        @param totalFitness: the sum of the fitness values of the population
        @return the selected individual
    """
    def __rouletteWheel(self, scores, totalFitness):
        i = 0
        selector = scores[0] / totalFitness
        r = random.uniform(0, 1)

        while selector < r:
            i += 1
            selector += scores[i] / totalFitness

        return self.population[i] 

    """ This methods generates a new generation that is used as a new population.
        @param individuals: list of genes selected for the reproduction process (possible parents)
        @param mutationProb: the probability of a mutation occurring
        @param crossProb: the probability of a crossover occurring
    """
    def produceNewGeneration(self, individuals, mutationProb, crossProb):
        parents = []
        numParents = int(len(individuals) * crossProb)
  
        if crossProb < 1:
            while numParents > 0:
                index = random.randint(0, len(individuals) - 1)
                parents.append(individuals.pop(index))
                numParents -= 1

            newPopulation = []
            numParents = len(parents)
            father = None
            mother = None

            # Performing the crossovers
            if numParents % 2 != 0:
                father = parents.pop(numParents - 1)
                mother = parents[random.randint(0, len(parents) - 1)]
                sons = self.__crossover(father, mother)
                newPopulation.append(sons[0])
                newPopulation.append(sons[1])

            while numParents > 0:
                mother = parents.pop(random.randint(0, len(parents) - 1))
                father = parents.pop(random.randint(0, len(parents) - 1))
                sons = self.__crossover(father, mother)
                newPopulation.append(sons[0])
                newPopulation.append(sons[1])
                numParents -= 2
        
        # Selecting the rest of parents
        for i in range(len(individuals)):
            newPopulation.append(individuals[i])

        # Performing the mutations
        for gene in newPopulation:
            self.__mutation(gene, mutationProb)
        
        self.population = newPopulation
                
    """ This method implements a one-point crossover between two genes.
        @param gene1: parent 1
        @param gene2: parent 2
        @return two new individuals as resulting of the crossover process
    """
    def __crossover(self, gene1, gene2):
        middle = int(len(gene1)/2)

        son1 = []
        son2 = []

        for i in range(middle):
            son1.append(gene1[i])
            son2.append(gene2[i])

        for i in range(middle, len(gene1)):
            son1.append(gene2[i])
            son2.append(gene1[i])

        return (son1, son2)

    """ This method implements the mutation process, it changes the content of a given allele.
        @param gene: the gene to be mutated
        @param mutationProb: the probability of a mutation occurring
    """
    def __mutation(self, gene, mutationProb):
        for i in range(len(gene)):
            if random.uniform(0, 1) <= mutationProb:
                if gene[i] == 1: 
                    gene[i] = 0
       
    """ This method shows the population on the screen """
    def showPopulation(self):
        for gene in self.population:
            print(gene)

    """ This method transforms a gene into a bag and shows the bags one on the screen """
    def showBags(self):
        for gene in self.population:
            bag = Bag()
            bag.makeMapping(self.items, gene)
            bag.show()
            print("------------------------")

    """ This method transforms the best gene into a bag and shows the bag one on the screen """
    def showBestBag(self):
        bag = Bag()
        bag.makeMapping(self.items, self.bestGene)
        print("The best fitness: ", self.bestFitness)
        print("The best generation: ", self.bestGeneration)
        bag.show()

