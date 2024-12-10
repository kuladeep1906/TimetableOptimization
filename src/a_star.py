import random
import time
import csv
import os
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import calculate_fitness

# Ensure the progress folder exists
if not os.path.exists("progress"):
    os.makedirs("progress")

# Function to initialize CSV log
def initialize_csv_log(algorithm_name):
    csv_path = f"progress/{algorithm_name}_progress.csv"  # Updated path to "progress" folder
    with open(csv_path, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Generation", "Current Best Fitness", "Overall Best Fitness", "Day", "Instances"])  # Write headers
    return csv_path

# Function to log progress for each generation to CSV
def log_progress_csv(csv_path, generation, current_best_fitness, best_fitness, day, instances):
    with open(csv_path, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([generation, current_best_fitness, best_fitness, day, instances])  # Append data to CSV

def a_star_algorithm(logger, max_iterations=100):
    # Start timing
    start_time = time.time()

    # Initialize CSV logging 
    csv_path = initialize_csv_log("A_Star")

    # Initialize the current state based on courses, rooms, timeslots, and days
    current_state = []
    for course in COURSES:
        for _ in range(course["instances_per_week"]):  # Create slots based on instances per week
            teacher = next(teacher for teacher in TEACHERS if teacher["name"] == course["teacher"])
            current_state.append({
                'course': course['name'],
                'room': random.choice(course['preferred_rooms']),
                'teacher': course['teacher'],
                'timeslot': random.choice(teacher['availability']),
                'day': random.choice(teacher['preferred_days']),
            })

    best_fitness = calculate_fitness(current_state)
    best_state = current_state.copy()

    for iteration in range(max_iterations):
        successors = []
        for _ in range(5):
            successor = []
            for course in COURSES:
                for _ in range(course["instances_per_week"]):
                    teacher = next(teacher for teacher in TEACHERS if teacher["name"] == course["teacher"])
                    successor.append({
                        'course': course['name'],
                        'room': random.choice(course['preferred_rooms']),
                        'teacher': course['teacher'],
                        'timeslot': random.choice(teacher['availability']),
                        'day': random.choice(teacher['preferred_days']),
                    })
            successors.append(successor)

        best_successor = max(successors, key=calculate_fitness)
        best_successor_fitness = calculate_fitness(best_successor)

        if best_successor_fitness > best_fitness:
            current_state = best_successor
            best_state = best_successor.copy()
            best_fitness = best_successor_fitness

        # Get day and instances information for logging
        unique_days = {entry['day'] for entry in current_state}
        day_instances = {day: sum(1 for entry in current_state if entry['day'] == day) for day in unique_days}

        logger.info(f"Iteration {iteration + 1}: Current Fitness = {best_successor_fitness}, Best Fitness = {best_fitness}")

        # Log progress to CSV for a random day in the current iteration
        if unique_days:
            random_day = random.choice(list(unique_days))
            log_progress_csv(csv_path, iteration + 1, best_successor_fitness, best_fitness, random_day, day_instances[random_day])

    elapsed_time = time.time() - start_time

    logger.info("Final Best Timetable Configuration (A*):")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}")

    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")

    return best_state, best_fitness, elapsed_time, csv_path  