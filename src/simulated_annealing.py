import random
import logging
from .fitness import evaluate_fitness
from data.input_data import TIMESLOTS, ROOMS, TEACHERS, COURSES

def run_simulated_annealing(solution, max_iterations=100, initial_temp=100, cooling_rate=0.95):
    """
    Performs simulated annealing optimization on a timetable solution.

    Args:
    - solution: list of dict, the initial timetable solution.
    - max_iterations: int, the maximum number of iterations.
    - initial_temp: float, the initial temperature.
    - cooling_rate: float, the rate at which temperature decreases.

    Returns:
    - best_solution: list of dict, the optimized solution.
    """
    current_solution = solution
    current_score = evaluate_fitness(current_solution)
    best_solution = current_solution
    best_score = current_score
    temperature = initial_temp

    logging.info("Starting Simulated Annealing...")
    logging.info(f"Initial score: {current_score}")

    for iteration in range(max_iterations):
        # Generate a neighbor solution by mutating the current solution
        neighbor_solution = mutate_solution(current_solution)
        neighbor_score = evaluate_fitness(neighbor_solution)

        # Calculate acceptance probability and decide to accept the neighbor
        delta = neighbor_score - current_score
        acceptance_prob = min(1, (2.718 ** (-delta / temperature)) if delta > 0 else 1)

        if acceptance_prob > random.random():
            current_solution = neighbor_solution
            current_score = neighbor_score

            # Update the best solution if the current is better
            if current_score < best_score:
                best_solution = current_solution
                best_score = current_score
                logging.info(f"New best solution at iteration {iteration + 1}: Score = {best_score}")

        # Decrease temperature
        temperature *= cooling_rate
        logging.info(f"Iteration {iteration + 1}: Current Score = {current_score}, Temperature = {temperature}")

    logging.info("Simulated Annealing completed.")
    logging.info(f"Final best score: {best_score}")
    return best_solution

def mutate_solution(solution):
    """
    Creates a neighbor solution by modifying a random entry in the timetable.

    Args:
    - solution: list of dict, representing the timetable.

    Returns:
    - neighbor_solution: list of dict, the modified solution.
    """
    neighbor_solution = [entry.copy() for entry in solution]  # Deep copy to avoid altering the original solution
    entry = random.choice(neighbor_solution)  # Select a random entry to modify

    # Mutate room to one that meets capacity needs
    students = next((c['students'] for c in COURSES if c['name'] == entry['course']), 0)
    entry['room'] = random.choice([room['name'] for room in ROOMS if room['capacity'] >= students])

    # Mutate timeslot
    entry['timeslot'] = random.choice(TIMESLOTS)

    # Mutate teacher based on availability in the new timeslot
    available_teachers = [teacher['name'] for teacher in TEACHERS if entry['timeslot'] in teacher['availability']]
    if available_teachers:
        entry['teacher'] = random.choice(available_teachers)

    return neighbor_solution
