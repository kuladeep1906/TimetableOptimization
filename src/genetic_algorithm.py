import logging
import random
from concurrent.futures import ThreadPoolExecutor
from .fitness import evaluate_fitness
from .crossover import crossover
from .mutation import mutate

logging.basicConfig(filename='timetable_optimization_output.txt', level=logging.INFO, format='%(message)s', force=True)

def select_population(population, fitness_scores, num_selected=20):
    """
    Selects a subset of the population based on fitness scores.
    """
    scored_population = list(zip(population, fitness_scores))
    scored_population.sort(key=lambda x: x[1])  # Sort by fitness score
    selected_population = [ind for ind, _ in scored_population[:num_selected]]
    return selected_population

def run_genetic_algorithm(initial_population, generations=20, population_size=30, mutation_rate=0.05):
    """
    Runs the genetic algorithm to evolve a full timetable solution.
    """
    population = initial_population

    for generation in range(generations):
        logging.info(f"Generation {generation + 1}")

        # Evaluate fitness in parallel for the entire timetable
        with ThreadPoolExecutor() as executor:
            fitness_scores = list(executor.map(evaluate_fitness, population))

        # Select top-performing individuals (full timetables)
        selected_population = select_population(population, fitness_scores, num_selected=population_size // 2)

        # Generate offspring through crossover
        offspring = []
        for i in range(0, len(selected_population), 2):
            if i + 1 < len(selected_population):
                parent1 = selected_population[i]
                parent2 = selected_population[i + 1]
                child1, child2 = crossover(parent1, parent2)
                offspring.extend([child1, child2])

        # Apply mutation on each offspring
        mutated_offspring = [mutate(individual, mutation_rate=mutation_rate) for individual in offspring]

        # Form the new population, keeping population size constant
        population = selected_population + mutated_offspring
        population = population[:population_size]

    # Final evaluation to find the best solution (full timetable)
    final_fitness_scores = list(map(evaluate_fitness, population))
    best_solution = population[final_fitness_scores.index(min(final_fitness_scores))]
    
    # Log final solution for review
    logging.info("Final GA Solution (full timetable): " + str(best_solution))
    return best_solution
