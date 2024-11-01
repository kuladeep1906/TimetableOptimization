import logging
import random
from .fitness import evaluate_fitness
from .mutation import mutate
from data.input_data import ROOMS, TIMESLOTS, TEACHERS

logging.basicConfig(filename='timetable_optimization_output.txt', level=logging.INFO, format='%(message)s')

def run_tabu_search(initial_solution, max_iterations=100, tabu_tenure=10):
    current_solution = initial_solution[:]  # Make a copy to avoid modifying the original
    best_solution = initial_solution[:]
    best_score = evaluate_fitness(current_solution)
    tabu_list = []

    for iteration in range(max_iterations):
        logging.info(f"Iteration {iteration + 1}: Current Best Score = {best_score}")

        # Generate neighbors by modifying each course in the full timetable
        neighbors = []
        for entry in current_solution:
            if not isinstance(entry, dict):
                logging.info("Invalid course entry format in run_tabu_search: " + str(entry))
                continue

            # Create a neighbor by mutating attributes in each entry
            neighbor_entry = entry.copy()
            if 'timeslot' in neighbor_entry:
                neighbor_entry['timeslot'] = random.choice(TIMESLOTS)
            if 'room' in neighbor_entry:
                neighbor_entry['room'] = random.choice(
                    [room['name'] for room in ROOMS if room['capacity'] >= 20]  # Example capacity filter
                )
            if 'teacher' in neighbor_entry:
                neighbor_entry['teacher'] = random.choice(
                    [teacher['name'] for teacher in TEACHERS if neighbor_entry['timeslot'] in teacher['availability']]
                )

            # Append the modified entry as part of a new full timetable
            neighbor_solution = current_solution[:]
            neighbor_solution[current_solution.index(entry)] = neighbor_entry
            neighbors.append(neighbor_solution)

        # Evaluate each neighbor and find the best one not in the tabu list
        best_neighbor = None
        best_neighbor_score = float('inf')
        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_score = evaluate_fitness(neighbor)
                if neighbor_score < best_neighbor_score:
                    best_neighbor = neighbor
                    best_neighbor_score = neighbor_score

        # Update current solution if a valid neighbor is found
        if best_neighbor:
            current_solution = best_neighbor[:]
            if len(tabu_list) >= tabu_tenure:
                tabu_list.pop(0)  # Maintain the size of the tabu list
            tabu_list.append(best_neighbor)

            # Update the best solution if the neighbor improves the score
            if best_neighbor_score < best_score:
                best_solution = best_neighbor[:]
                best_score = best_neighbor_score

        logging.info(f"Best solution after iteration {iteration + 1}: {best_solution}")

    return best_solution
