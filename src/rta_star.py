from .fitness import evaluate_fitness
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
import random

def refine_with_rta_star(individual, max_iterations=100):
    current_solution = individual
    current_score = evaluate_fitness(current_solution)

    for iteration in range(max_iterations):
        problem_entries = identify_problems(current_solution)
        if not problem_entries:
            break

        problem_entry = random.choice(problem_entries)
        alternatives = generate_alternatives(problem_entry, current_solution)
        best_alternative = min(alternatives, key=evaluate_fitness)
        best_score = evaluate_fitness(best_alternative)

        if best_score < current_score:
            current_solution = best_alternative
            current_score = best_score

    return current_solution

def identify_problems(solution):
    problems = []
    for entry in solution:
        course = entry['course']
        room = entry['room']
        timeslot = entry['timeslot']
        teacher = entry['teacher']
        students = next(c['students'] for c in COURSES if c['name'] == course)

        room_data = next(r for r in ROOMS if r['name'] == room)
        if students > room_data['capacity']:
            problems.append(entry)

        teacher_data = next(t for t in TEACHERS if t['name'] == teacher)
        if timeslot not in teacher_data['availability']:
            problems.append(entry)

    return problems

def generate_alternatives(entry, solution):
    alternatives = []
    course = entry['course']
    students = next(c['students'] for c in COURSES if c['name'] == course)

    # Generate room alternatives
    for room in [r['name'] for r in ROOMS if r['capacity'] >= students]:
        new_solution = [e.copy() for e in solution]
        for e in new_solution:
            if e['course'] == course:
                e['room'] = room
        alternatives.append(new_solution)

    # Generate timeslot alternatives
    for timeslot in TIMESLOTS:
        new_solution = [e.copy() for e in solution]
        for e in new_solution:
            if e['course'] == course:
                e['timeslot'] = timeslot
        alternatives.append(new_solution)

    # Generate teacher alternatives
    for teacher in [t['name'] for t in TEACHERS if timeslot in t['availability']]:
        new_solution = [e.copy() for e in solution]
        for e in new_solution:
            if e['course'] == course:
                e['teacher'] = teacher
        alternatives.append(new_solution)

    return alternatives
