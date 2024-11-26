import random
import time
import csv  # For progress logging
from collections import deque
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

def tabu_search(logger, max_iterations=300, tabu_tenure=10, neighbors_to_generate=5):
    # Start timing
    start_time = time.time()
    
    # Initialize CSV logging
    csv_path = initialize_csv_log("tabu_search")
    
    # Initialize a random solution
    current_state = [
        {
            'course': course['name'],
            'room': random.choice(course['preferred_rooms']),
            'teacher': course['teacher'],
            'timeslot': random.choice(next(teacher for teacher in TEACHERS if teacher['name'] == course['teacher'])['availability'])
        }
        for course in COURSES
    ]
    
    # Calculate fitness of the initial solution
    current_fitness = calculate_fitness(current_state)
    best_state = current_state
    best_fitness = current_fitness

    # Initialize the tabu list
    tabu_list = deque(maxlen=tabu_tenure)

    for iteration in range(max_iterations):
        logger.info(f"Iteration {iteration + 1}: Current Fitness = {current_fitness}, Best Fitness = {best_fitness}")
        log_progress_csv(csv_path, iteration + 1, current_fitness, best_fitness)

        # Generate neighbors and avoid moves in the tabu list
        neighbors = []
        for i in range(neighbors_to_generate):
            neighbor = current_state.copy()
            for entry in neighbor:
                # Randomly assign room and timeslot
                entry['room'] = random.choice([room['name'] for room in ROOMS if room['capacity'] >= next(course['students'] for course in COURSES if course['name'] == entry['course'])])
                entry['timeslot'] = random.choice(next(teacher for teacher in TEACHERS if teacher['name'] == entry['teacher'])['availability'])

            # Skip neighbors that are in the tabu list
            neighbor_tuple = tuple((entry['course'], entry['room'], entry['timeslot']) for entry in neighbor)
            if neighbor_tuple not in tabu_list:
                neighbors.append((neighbor, calculate_fitness(neighbor)))

        # If no non-tabu neighbors, skip to the next iteration
        if not neighbors:
            logger.info("All neighbors are tabu, moving to next iteration.")
            continue

        # Find the best non-tabu neighbor
        best_neighbor, best_neighbor_fitness = max(neighbors, key=lambda x: x[1])

        # Log details of the best neighbor
        logger.info(f"Best Neighbor Found: Fitness = {best_neighbor_fitness}")
        for entry in best_neighbor:
            logger.info(f"    Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

        # Update the current state to the best neighbor
        current_state, current_fitness = best_neighbor, best_neighbor_fitness

        # Update the tabu list with the move just made
        tabu_list.append(tuple((entry['course'], entry['room'], entry['timeslot']) for entry in current_state))
        
        # Update the best global state if an improvement is found
        if current_fitness > best_fitness:
            best_state, best_fitness = current_state, current_fitness
            logger.info(f"Updated Global Best State with Fitness = {best_fitness}")

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Log the final best state
    logger.info("Final Best Timetable Configuration (Tabu Search):")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")

    # Return the best state, fitness, elapsed time, and CSV path
    return best_state, best_fitness, elapsed_time, csv_path
