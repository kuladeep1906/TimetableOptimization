import random
import time
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import calculate_fitness

def rta_star_algorithm(logger, max_iterations=100):
    # Start timing
    start_time = time.time()

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

        logger.info(f"Iteration {iteration + 1}: Current Fitness = {best_fitness}")

    elapsed_time = time.time() - start_time

    logger.info("Final Best Timetable Configuration (RTA*):")
    for entry in best_state:
        logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")

    # Append final best results to final_output.log for comparison
   # with open("logs/final_output.log", "a") as log_file:
    #    log_file.write("\nRTA* Algorithm - Final Iteration Results\n")
    #    log_file.write(f"Best Fitness: {best_fitness}\n")
   #     log_file.write(f"Time Taken: {elapsed_time:.2f} seconds\n")
   #     log_file.write("Best Timetable Configuration:\n")
   #     for entry in best_state:
   #         log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}\n")

    return best_state, best_fitness, elapsed_time  # Return elapsed time as the third value
