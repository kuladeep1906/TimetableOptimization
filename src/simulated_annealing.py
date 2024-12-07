import random
import math
import time
import csv  # Import CSV for logging
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import calculate_fitness
import os
from collections import Counter

# Ensure the progress folder exists
if not os.path.exists("progress"):
    os.makedirs("progress")

# Function to initialize CSV log
def initialize_csv_log(algorithm_name):
    csv_path = f"progress/{algorithm_name}_progress.csv"  # Updated path to "progress" folder
    with open(csv_path, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Generation", "Temperature", "Current Best Fitness", "Overall Best Fitness", "Cooling Rate"])  # Write headers
    return csv_path

# Function to log progress for each generation to CSV
def log_progress_csv(csv_path, generation, temperature, current_best_fitness, best_fitness, cooling_rate):
    with open(csv_path, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([generation, temperature, current_best_fitness, best_fitness, cooling_rate])  # Append data to CSV

def simulated_annealing(logger, initial_temp=1000, initial_cooling_rate=0.95, max_iterations=1000):
    start_time = time.time()
    csv_path = initialize_csv_log("simulated_annealing")

    # Initialize parameters
    current_state = []
    for course in COURSES:
        for _ in range(course['instances_per_week']):
            teacher = next(teacher for teacher in TEACHERS if teacher['name'] == course['teacher'])
            current_state.append({
                'course': course['name'],
                'room': random.choice(course['preferred_rooms']),
                'teacher': teacher['name'],
                'timeslot': random.choice(teacher['availability']),
                'day': random.choice(teacher['preferred_days']),
            })

    current_fitness = calculate_fitness(current_state)
    best_state = current_state
    best_fitness = current_fitness
    temperature = initial_temp
    cooling_rate = initial_cooling_rate

    for iteration in range(max_iterations):
        # Generate a neighbor state
        neighbor = []
        for course in COURSES:
            for _ in range(course['instances_per_week']):
                teacher = next(teacher for teacher in TEACHERS if teacher['name'] == course['teacher'])
                neighbor.append({
                    'course': course['name'],
                    'room': random.choice(course['preferred_rooms']),
                    'teacher': teacher['name'],
                    'timeslot': random.choice(teacher['availability']),
                    'day': random.choice(teacher['preferred_days']),
                })

        neighbor_fitness = calculate_fitness(neighbor)

        # Acceptance decision
        diff = (neighbor_fitness - current_fitness) / max(temperature, 1e-6)
        clamped_diff = max(min(diff, 700), -700)
        acceptance_probability = math.exp(clamped_diff)

        if neighbor_fitness > current_fitness or random.random() < acceptance_probability:
            current_state, current_fitness = neighbor, neighbor_fitness
            if current_fitness > best_fitness:
                best_state, best_fitness = current_state, current_fitness

        # Log progress
        logger.info(f"Iteration {iteration + 1}, Temperature: {temperature:.2f}, Current Fitness: {current_fitness}, Best Fitness: {best_fitness}, Cooling Rate: {cooling_rate:.2f}")
        log_progress_csv(csv_path, iteration + 1, temperature, current_fitness, best_fitness, cooling_rate)

        # Adjust temperature using logarithmic cooling schedule
        temperature = initial_temp / (1 + math.log(1 + iteration))
        if temperature < 1e-3:
            logger.info("Temperature dropped below threshold. Stopping iterations.")
            break

    elapsed_time = time.time() - start_time

    # Final results logging
    logger.info("Final Best Timetable Configuration (Simulated Annealing):")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}")
    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")

    return best_state, best_fitness, elapsed_time, csv_path
