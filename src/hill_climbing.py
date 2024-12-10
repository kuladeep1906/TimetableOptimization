import random
import time
import csv
import os
from data.input_data import COURSES, TEACHERS, ROOMS
from .fitness import calculate_fitness

# Ensure the progress folder exists
if not os.path.exists("progress"):
    os.makedirs("progress")

# Function to initialize CSV log
def initialize_csv_log(algorithm_name):
    csv_path = f"progress/{algorithm_name}_progress.csv" 
    with open(csv_path, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Generation", "Current Best Fitness", "Overall Best Fitness", "Day", "Instances"]) 
    return csv_path

# Function to log progress for each generation to CSV
def log_progress_csv(csv_path, generation, current_best_fitness, best_fitness, day, instances):
    with open(csv_path, mode='a', newline='') as file:  
        writer = csv.writer(file)
        writer.writerow([generation, current_best_fitness, best_fitness, day, instances])

def hill_climbing(logger, max_iterations=1000, neighbors_to_generate=5, restart_attempts=30):
    # Start timing
    start_time = time.time()

    # Initialize CSV logging 
    csv_path = initialize_csv_log("hill_climbing")
     
    overall_best_fitness = float('-inf') 
    best_state = None
    best_fitness = float('-inf')
    generation = 0

    for attempt in range(restart_attempts):
        # Initialize a random solution 
        current_state = []
        for course in COURSES:
            for _ in range(course.get("instances_per_week", 1)): 
                teacher = next(teacher for teacher in TEACHERS if teacher['name'] == course['teacher'])
                current_state.append({
                    'course': course['name'],
                    'room': random.choice(course['preferred_rooms']),
                    'teacher': course['teacher'],
                    'timeslot': random.choice(teacher['availability']),
                    'day': random.choice(teacher['preferred_days']),
                })
        
        current_fitness = calculate_fitness(current_state)
        logger.info(f"Attempt {attempt + 1}: Initial Fitness = {current_fitness}")

        
        if best_state is None:
            best_state = current_state
            best_fitness = current_fitness

        # Log the initial state
        generation += 1
        log_progress_csv(csv_path, generation, current_fitness, overall_best_fitness, current_state[0]['day'], len(current_state))

        
        for iteration in range(max_iterations):
            generation += 1
            logger.info(f"Attempt {attempt + 1}, Iteration {iteration + 1}: Current Fitness = {current_fitness}, Best Fitness = {best_fitness}")

            # Generate neighbors
            neighbors = []
            for _ in range(neighbors_to_generate):
                neighbor = []
                for entry in current_state:
                    neighbor.append({
                        'course': entry['course'],
                        'room': random.choice([room['name'] for room in ROOMS if room['capacity'] >= next(course['students'] for course in COURSES if course['name'] == entry['course'])]),
                        'teacher': entry['teacher'],
                        'timeslot': random.choice(next(teacher for teacher in TEACHERS if teacher['name'] == entry['teacher'])['availability']),
                        'day': random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
                    })
                neighbors.append((neighbor, calculate_fitness(neighbor)))

           
            best_neighbor, best_neighbor_fitness = max(neighbors, key=lambda x: x[1])
            logger.info(f"Best Neighbor Fitness = {best_neighbor_fitness}")

           
            if best_neighbor_fitness > current_fitness:
                current_state, current_fitness = best_neighbor, best_neighbor_fitness
                log_progress_csv(csv_path, generation, current_fitness, overall_best_fitness, current_state[0]['day'], len(current_state))
            else:
                logger.info("No improvement found. Ending iteration.")
                break

            # Update the best state if a better fitness is found
            if current_fitness > best_fitness:
                best_state, best_fitness = current_state, current_fitness
                logger.info(f"Updated Best Fitness = {best_fitness}")

           
            if current_fitness > overall_best_fitness:
                overall_best_fitness = current_fitness
                logger.info(f"Updated Overall Best Fitness = {overall_best_fitness}") 

            
            log_progress_csv(csv_path, generation, current_fitness, overall_best_fitness, current_state[0]['day'], len(current_state))

        
        log_progress_csv(csv_path, generation, current_fitness, overall_best_fitness, current_state[0]['day'], len(current_state))

    # Elapsed time calculation
    elapsed_time = time.time() - start_time

    logger.info("Final Best Timetable:")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}")
    
    logger.info(f"Elapsed Time: {elapsed_time:.2f} seconds")

    return best_state, overall_best_fitness, elapsed_time, csv_path
