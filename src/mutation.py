import logging
import random
from data.input_data import ROOMS, TIMESLOTS, TEACHERS, COURSES

logging.basicConfig(filename='timetable_optimization_output.txt', level=logging.INFO, format='%(message)s')

def validate_entry(entry):
    required_keys = {'course', 'room', 'timeslot', 'teacher'}
    return isinstance(entry, dict) and required_keys.issubset(entry.keys())

def mutate(individual, mutation_rate=0.05):
    """
    Mutates an individual timetable solution.
    """
    if isinstance(individual, dict):
        individual = [individual]

    for entry in individual:
        if not validate_entry(entry):
            continue

        students = next((c['students'] for c in COURSES if c['name'] == entry['course']), 0)

        if random.random() < mutation_rate:
            entry['room'] = random.choice([room['name'] for room in ROOMS if room['capacity'] >= students])
        if random.random() < mutation_rate:
            entry['timeslot'] = random.choice(TIMESLOTS)
        if random.random() < mutation_rate:
            available_teachers = [t['name'] for t in TEACHERS if entry['timeslot'] in t['availability']]
            if available_teachers:
                entry['teacher'] = random.choice(available_teachers)

    logging.info("Mutated Individual: " + str(individual))
    return individual
