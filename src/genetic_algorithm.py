import random
from deap import base, creator, tools, algorithms
from src.fitness import evaluate  # Use the updated fitness function
from src.mutation import mutate_timetable
from src.selection import select_best
from src.timetable import Timetable
from data.input_data import TIMESLOTS  # Import TIMESLOTS for room/teacher checks

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Check if the generated timetable is conflict-free
def is_valid_schedule(timetable):
    """
    Check the generated timetable for room and teacher conflicts.
    """
    room_usage = {timeslot: [] for timeslot in TIMESLOTS}
    teacher_usage = {timeslot: [] for timeslot in TIMESLOTS}

    for course, room, teacher, timeslot in timetable:
        if room in room_usage[timeslot] or teacher in teacher_usage[timeslot]:
            return False  # Conflict detected
        room_usage[timeslot].append(room)
        teacher_usage[timeslot].append(teacher)
    
    return True

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, lambda: Timetable().timetable)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate_timetable)
toolbox.register("select", tools.selTournament, tournsize=3)

def adaptive_mutation(gen, max_gen):
    """
    Dynamically adjust the mutation rate. Start high and decrease over generations.
    """
    initial_mutation_rate = 0.3
    final_mutation_rate = 0.05
    return initial_mutation_rate - ((initial_mutation_rate - final_mutation_rate) * (gen / max_gen))

def run_genetic_algorithm(population_size=200, generations=100, crossover_prob=0.8, mutation_prob=0.2, elite_size=2):
    """
    Run the Genetic Algorithm with Elitism.
    """
    population = toolbox.population(n=population_size)

    # Add Elitism: Preserve the best individuals
    for gen in range(generations):
        offspring = toolbox.select(population, len(population) - elite_size)
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < crossover_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate invalid offspring
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select elite individuals and replace them in the population
        elite_individuals = tools.selBest(population, elite_size)
        population[:] = offspring + elite_individuals

        # Optional: Log progress or stats

    return tools.selBest(population, 1)[0]  # Return the best individual

