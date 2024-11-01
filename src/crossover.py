import random
import logging

def crossover(parent1, parent2):
    logging.info("Parent 1 before crossover: " + str(parent1))
    logging.info("Parent 2 before crossover: " + str(parent2))
    
    split_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:split_point] + parent2[split_point:]
    child2 = parent2[:split_point] + parent1[split_point:]

    # Log the structure of the offspring
    logging.info("Child 1 after crossover: " + str(child1))
    logging.info("Child 2 after crossover: " + str(child2))

    return child1, child2
