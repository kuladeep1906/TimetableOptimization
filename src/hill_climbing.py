import random
import time
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import calculate_fitness

def hill_climbing(logger, max_iterations=1000, neighbors_to_generate=5, restart_attempts=3):
    # Start timing
    start_time = time.time()
    
    best_state = None
    best_fitness = float('-inf')
    
    for attempt in range(restart_attempts):
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
        
        current_fitness = calculate_fitness(current_state)

        # Initialize best_state and best_fitness if not set
        if best_state is None:
            best_state = current_state
            best_fitness = current_fitness

        logger.info(f"Attempt {attempt + 1} - Initial State: Fitness = {current_fitness}")
        for entry in current_state:
            logger.info(f"    Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

        for iteration in range(max_iterations):
            logger.info(f"Attempt {attempt + 1}, Iteration {iteration + 1}: Current Fitness = {current_fitness}, Best Fitness = {best_fitness}")

            # Generate multiple neighbors
            neighbors = []
            for i in range(neighbors_to_generate):
                neighbor = current_state.copy()
                for entry in neighbor:
                    entry['room'] = random.choice([room['name'] for room in ROOMS if room['capacity'] >= next(course['students'] for course in COURSES if course['name'] == entry['course'])])
                    entry['timeslot'] = random.choice(next(teacher for teacher in TEACHERS if teacher['name'] == entry['teacher'])['availability'])
                neighbors.append(neighbor)
                neighbor_fitness = calculate_fitness(neighbor)
                
                # Log each neighbor's fitness and configuration
                logger.info(f"    Neighbor {i + 1}: Fitness = {neighbor_fitness}")
                for entry in neighbor:
                    logger.info(f"        Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

            # Find the best neighbor
            best_neighbor = max(neighbors, key=calculate_fitness)
            best_neighbor_fitness = calculate_fitness(best_neighbor)

            # Log the best neighbor found in this iteration
            logger.info(f"    Best Neighbor: Fitness = {best_neighbor_fitness}")
            for entry in best_neighbor:
                logger.info(f"        Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

            # Accept the best neighbor if it improves fitness
            if best_neighbor_fitness > current_fitness:
                current_state, current_fitness = best_neighbor, best_neighbor_fitness
                logger.info(f"    Accepted New State with Improved Fitness = {current_fitness}")
            else:
                # If no improvement, stop this attempt
                logger.info("    No Improvement Found - Ending This Attempt")
                break

            # Update the global best solution if found
            if current_fitness > best_fitness:
                best_state, best_fitness = current_state, current_fitness
                logger.info(f"    Updated Global Best State with Fitness = {best_fitness}")

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Log the final best state after all restarts
    logger.info("Final Best Timetable Configuration (Hill Climbing):")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")

   
    return best_state, best_fitness, elapsed_time
