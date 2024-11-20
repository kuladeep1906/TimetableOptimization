import random
import time
import csv  # Import CSV for logging
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import calculate_fitness

import csv
import os

# Ensure the progress folder exists
if not os.path.exists("progress"):
    os.makedirs("progress")

# Function to initialize CSV log
def initialize_csv_log(algorithm_name):
    csv_path = f"progress/{algorithm_name}_progress.csv"  # Updated path to "progress" folder
    with open(csv_path, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Generation", "Current Best Fitness", "Overall Best Fitness"])  # Write headers
    return csv_path

# Function to log progress for each generation to CSV
def log_progress_csv(csv_path, generation, current_best_fitness, best_fitness):
    with open(csv_path, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([generation, current_best_fitness, best_fitness])  # Append data to CSV

def rta_star_algorithm(logger, max_iterations=100):
    # Start timing
    start_time = time.time()

    # Initialize CSV logging
    csv_path = initialize_csv_log("RTA_Star")

    current_state = [
        {
            'course': course['name'],
            'room': random.choice(course['preferred_rooms']),
            'teacher': course['teacher'],
            'timeslot': random.choice(next(teacher for teacher in TEACHERS if teacher['name'] == course['teacher'])['availability'])
        }
        for course in COURSES
    ]

    best_fitness = calculate_fitness(current_state)
    best_state = current_state.copy()

    for iteration in range(max_iterations):
        successors = []
        for _ in range(5):
            successor = current_state.copy()
            for entry in successor:
                entry['room'] = random.choice([room['name'] for room in ROOMS if room['capacity'] >= next(course['students'] for course in COURSES if course['name'] == entry['course'])])
                entry['timeslot'] = random.choice(next(teacher for teacher in TEACHERS if teacher['name'] == entry['teacher'])['availability'])
            successors.append(successor)

        best_successor = max(successors, key=calculate_fitness)
        best_successor_fitness = calculate_fitness(best_successor)

        if best_successor_fitness > best_fitness:
            current_state = best_successor
            best_state = best_successor.copy()
            best_fitness = best_successor_fitness

        logger.info(f"Iteration {iteration + 1}: Current Fitness = {best_successor_fitness}, Best Fitness = {best_fitness}")

        # Log progress to CSV
        log_progress_csv(csv_path, iteration + 1, best_successor_fitness, best_fitness)

    elapsed_time = time.time() - start_time

    logger.info("Final Best Timetable Configuration (RTA*):")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")

    return best_state, best_fitness, elapsed_time, csv_path  # Return CSV path as part of the results
