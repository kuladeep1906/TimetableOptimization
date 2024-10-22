import random
from deap import creator

def crossover(parent1, parent2):
    """
    Perform a one-point crossover between two timetables (parents).
    The offspring should also be of type creator.Individual.
    """
    index = random.randint(1, len(parent1) - 1)
    child1 = creator.Individual(parent1[:index] + parent2[index:])
    child2 = creator.Individual(parent2[:index] + parent1[index:])
    return child1, child2
