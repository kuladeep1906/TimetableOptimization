import random
import math
import time
import csv  # Import CSV for logging
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import calculate_fitness

import os

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

def simulated_annealing(logger, initial_temp=1000, initial_cooling_rate=0.95, max_iterations=1000, stagnation_limit=50):
    # Start timing
    start_time = time.time()

    # Initialize CSV logging
    csv_path = initialize_csv_log("simulated_annealing")

    # Create an initial random solution
    current_state = [
        {
            'course': course['name'],
            'room': random.choice(course['preferred_rooms']),
            'teacher': course['teacher'],
            'timeslot': random.choice(next(teacher for teacher in TEACHERS if teacher['name'] == course['teacher'])['availability'])
        }
        for course in COURSES
    ]
    
    current_fitness = calculate_fitness(current_state)
    best_state = current_state
    best_fitness = current_fitness
    temperature = initial_temp
    cooling_rate = initial_cooling_rate
    stagnation_counter = 0

    for iteration in range(max_iterations):
        # Generate a neighbor state by making slight modifications
        neighbor = current_state.copy()
        for entry in neighbor:
            entry['room'] = random.choice(
                [room['name'] for room in ROOMS if room['capacity'] >= next(course['students'] for course in COURSES if course['name'] == entry['course'])]
            )
            entry['timeslot'] = random.choice(
                next(teacher for teacher in TEACHERS if teacher['name'] == entry['teacher'])['availability']
            )
        
        neighbor_fitness = calculate_fitness(neighbor)

        # Handle large exponent issues by clamping the difference
        diff = (neighbor_fitness - current_fitness) / max(temperature, 1e-6)
        clamped_diff = max(min(diff, 700), -700)  # Clamp values to avoid overflow
        acceptance_probability = math.exp(clamped_diff)

        # Decide to accept the neighbor state based on fitness or probability
        if neighbor_fitness > current_fitness or random.random() < acceptance_probability:
            current_state, current_fitness = neighbor, neighbor_fitness
            stagnation_counter = 0  # Reset stagnation counter on improvement
            if current_fitness > best_fitness:
                best_state, best_fitness = current_state, current_fitness
        else:
            stagnation_counter += 1  # Increment stagnation counter if no improvement

        # Log progress for this iteration
        logger.info(f"Iteration {iteration + 1}, Temperature: {temperature:.2f}, Current Fitness: {current_fitness}, Best Fitness: {best_fitness}, Cooling Rate: {cooling_rate:.2f}")
        log_progress_csv(csv_path, iteration + 1, temperature, current_fitness, best_fitness, cooling_rate)

        # Adaptive cooling adjustment
        if stagnation_counter > stagnation_limit:
            cooling_rate = min(cooling_rate + 0.01, 0.99)  # Slow cooling if stagnant
            logger.info(f"Stagnation detected. Adjusting cooling rate to {cooling_rate:.2f}")
        else:
            cooling_rate = max(cooling_rate - 0.01, 0.90)  # Faster cooling if improving

        # Update temperature based on the adaptive cooling rate
        temperature *= cooling_rate
        if temperature < 1e-3:
            logger.info("Temperature dropped below threshold. Stopping iterations.")
            break

        # Introduce diversity by shuffling every 10 iterations
        if iteration % 10 == 0:
            random.shuffle(current_state)

    elapsed_time = time.time() - start_time

    # Logging final results to the logger
    logger.info("Final Best Timetable Configuration (Simulated Annealing):")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")
    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")

    return best_state, best_fitness, elapsed_time, csv_path  # Return CSV path for visualization
