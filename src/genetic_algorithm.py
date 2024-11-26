import random
import time
import csv
import os
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import calculate_fitness

# Constants
MUTATION_RATE = 0.01
ELITISM_RATE = 0.15
STAGNATION_LIMIT = 10

# Ensure the progress folder exists
if not os.path.exists("progress"):
    os.makedirs("progress")

# Function to initialize CSV log
def initialize_csv_log(algorithm_name):
    csv_path = f"progress/{algorithm_name}_progress.csv"  # Updated path to "progress" folder
    with open(csv_path, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["Generation", "Current Best Fitness", "Overall Best Fitness", "Average Fitness"])  # Added "Average Fitness"
    return csv_path

# Function to log progress for each generation to CSV
def log_progress_csv(csv_path, generation, current_best_fitness, best_fitness, avg_fitness):
    with open(csv_path, mode="a") as file:
        writer = csv.writer(file)
        writer.writerow([generation, current_best_fitness, best_fitness, avg_fitness])  # Log average fitness as well

def create_initial_population(size):
    population = []
    for _ in range(size):
        timetable = []
        for course in COURSES:
            teacher = next(teacher for teacher in TEACHERS if teacher["name"] == course["teacher"])
            room = random.choice(course["preferred_rooms"])
            timeslot = random.choice(teacher["availability"])
            timetable.append(
                {
                    "course": course["name"],
                    "room": room,
                    "teacher": teacher["name"],
                    "timeslot": timeslot,
                }
            )
        population.append(timetable)
    return population

def selection_with_elitism(population, retain_rate=ELITISM_RATE):
    population.sort(key=calculate_fitness, reverse=True)
    retain_length = int(len(population) * retain_rate)
    selected = population[:retain_length]
    remaining = population[retain_length:]
    selected.extend(random.sample(remaining, len(population) - retain_length))
    return selected

def two_point_crossover(parent1, parent2):
    point1, point2 = sorted(random.sample(range(len(parent1)), 2))
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

def mutate(timetable):
    for entry in timetable:
        if random.random() < MUTATION_RATE:
            teacher = next(teacher for teacher in TEACHERS if teacher["name"] == entry["teacher"])
            entry["timeslot"] = random.choice(teacher["availability"])
            entry["room"] = random.choice(
                [room["name"] for room in ROOMS if room["capacity"] >= next(course["students"] for course in COURSES if course["name"] == entry["course"])]
            )
    return timetable

def genetic_algorithm(logger, population_size=50, generations=70):
    start_time = time.time()
    population = create_initial_population(population_size)
    
    # Initialize CSV logging
    csv_path = initialize_csv_log("genetic_algorithm")

    best_timetable = max(population, key=calculate_fitness)
    best_fitness = calculate_fitness(best_timetable)
    stagnation_counter = 0

    for generation in range(generations):
        # Calculate average fitness for the population
        avg_fitness = sum(calculate_fitness(t) for t in population) / len(population)
        
        # Elitism and reproduction
        population = selection_with_elitism(population)
        new_population = population[:int(len(population) * ELITISM_RATE)]
        
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = two_point_crossover(parent1, parent2)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))

        population = new_population

        # Evaluate the new population
        current_best_timetable = max(population, key=calculate_fitness)
        current_best_fitness = calculate_fitness(current_best_timetable)
        
        if current_best_fitness > best_fitness:
            best_timetable, best_fitness = current_best_timetable, current_best_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Handle stagnation by introducing diversity
        if stagnation_counter >= STAGNATION_LIMIT:
            logger.info("Stagnation detected. Introducing new random individuals.")
            for _ in range(population_size // 5):  # Replace 20% of the population
                population[random.randint(0, population_size - 1)] = random.choice(create_initial_population(1))
            stagnation_counter = 0

        # Log fitness to CSV for visualization
        log_progress_csv(csv_path, generation + 1, current_best_fitness, best_fitness, avg_fitness)

        # Log progress for debugging
        logger.info(f"Generation {generation + 1}: Best Fitness = {best_fitness}, Avg Fitness = {avg_fitness:.2f}")
        logger.info("Best Timetable Configuration for this Generation:")
        for entry in best_timetable:
            logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

    # Capture end time and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    return best_timetable, best_fitness, elapsed_time, csv_path  # Return CSV path for visualization
