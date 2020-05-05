#!../bin/python

import sys
sys.path.append('classes')

from geneticAlg import GA
from enums import FitnessType

# Constants:

MUTATION_RATE = 0.06
CROSS_RATE = 0.7
POPULATION_SIZE = 300
NUMBER_OF_GENERATIONS = 500
#FITNESS_TYPE = FitnessType.PENALIZING
FITNESS_TYPE = FitnessType.REPAIRING

def main():
    try:   
        for i in range(10):
            exp = GA()
            exp.createPopulation(POPULATION_SIZE)
#            exp.showPopulation()

            generations = 0
            
            while generations < NUMBER_OF_GENERATIONS: 
                parents = exp.selectParents(POPULATION_SIZE, FITNESS_TYPE)
                exp.produceNewGeneration(parents, MUTATION_RATE, CROSS_RATE)
                generations += 1

            print("execution: ", i)
            exp.showBestBag()
            print("---------------")

    except RuntimeError as error: 
        print('Caught this error: ' + repr(error))
        raise 
    except Exception as excp:
        print('Caught this exception: ' + repr(excp))
        raise 

if __name__ == '__main__':
    main()
