import random
from src.fitness import evaluate  # Use the updated fitness function
from src.timetable import Timetable
from data.input_data import TIMESLOTS

def is_valid_schedule(timetable):
    """
    Check if the room and teacher are available at the given timeslot.
    """
    room_usage = {timeslot: [] for timeslot in TIMESLOTS}
    teacher_usage = {timeslot: [] for timeslot in TIMESLOTS}

    for course, room, teacher, timeslot in timetable:
        if room in room_usage[timeslot] or teacher in teacher_usage[timeslot]:
            return False  # Conflict found (either room or teacher conflict)
        room_usage[timeslot].append(room)
        teacher_usage[timeslot].append(teacher)

    return True

def rta_star(initial_solution, max_depth=5, max_iterations=1000):
    """
    Real-Time A* (RTA*) Algorithm to optimize the timetable scheduling problem.
    """
    current_solution = initial_solution
    best_solution = current_solution
    best_fitness = evaluate(current_solution.get_timetable_entries())[0]

    for iteration in range(max_iterations):
        neighbors = []
        for _ in range(max_depth):
            neighbor = Timetable()
            neighbor.mutate()

            # Validate if the new schedule is conflict-free
            if is_valid_schedule(neighbor.get_timetable_entries()):
                fitness = evaluate(neighbor.get_timetable_entries())[0]
                neighbors.append((neighbor, fitness))

        # Sort neighbors by fitness (highest first)
        if neighbors:
            neighbors.sort(key=lambda x: x[1], reverse=True)
            best_neighbor = neighbors[0]

            # Only accept if the best neighbor improves the fitness
            if best_neighbor[1] > best_fitness:
                current_solution = best_neighbor[0]
                best_fitness = best_neighbor[1]
                best_solution = current_solution

    return best_solution
