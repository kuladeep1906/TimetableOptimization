import random
import math
import time  # Import time to track elapsed time
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import calculate_fitness

def simulated_annealing(logger, initial_temp=1000, cooling_rate=0.95, max_iterations=1000):
    # Start timing
    start_time = time.time()

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

    for iteration in range(max_iterations):
        neighbor = current_state.copy()
        for entry in neighbor:
            entry['room'] = random.choice([room['name'] for room in ROOMS if room['capacity'] >= next(course['students'] for course in COURSES if course['name'] == entry['course'])])
            entry['timeslot'] = random.choice(next(teacher for teacher in TEACHERS if teacher['name'] == entry['teacher'])['availability'])
        
        neighbor_fitness = calculate_fitness(neighbor)

        if neighbor_fitness > current_fitness or math.exp((neighbor_fitness - current_fitness) / temperature) > random.random():
            current_state, current_fitness = neighbor, neighbor_fitness
            if current_fitness > best_fitness:
                best_state, best_fitness = current_state, current_fitness

        logger.info(f"Iteration {iteration + 1}, Temperature: {temperature:.2f}, Current Fitness: {current_fitness}, Best Fitness: {best_fitness}")
        
        temperature *= cooling_rate
        if temperature < 1e-3:
            break

    elapsed_time = time.time() - start_time

    # Logging final results to the logger
    logger.info("Final Best Timetable Configuration (Simulated Annealing):")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")
    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")

  
    return best_state, best_fitness, elapsed_time  # Return elapsed time as the third value
