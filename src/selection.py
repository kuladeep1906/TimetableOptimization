import random
from .fitness import evaluate_fitness

def select_population(population, num_selected=20):
    """
    Select a subset of the population for crossover based on their fitness.
    Uses a tournament selection mechanism where the fittest individuals are more likely to be chosen.
    """
    selected = []
    for _ in range(num_selected):
        # Randomly select a few individuals for the tournament.
        tournament = random.sample(population, k=5)

        # Evaluate fitness for each tournament participant.
        tournament_fitness = [(individual, evaluate_fitness(individual)) for individual in tournament]

        # Choose the winner of the tournament (individual with the lowest fitness score).
        winner = min(tournament_fitness, key=lambda x: x[1])[0]
        selected.append(winner)
    
    return selected
