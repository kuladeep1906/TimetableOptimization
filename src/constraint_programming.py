import random
from data.input_data import COURSES, ROOMS, TEACHERS, TIMESLOTS
import logging

logging.basicConfig(filename='timetable_optimization_output.txt', level=logging.INFO, format='%(message)s')

def generate_individual():
    individual = []
    for course in COURSES:
        # Check if course is correctly treated as a dictionary
        if isinstance(course, dict) and 'students' in course:
            room_options = [r['name'] for r in ROOMS if r['capacity'] >= course['students']]
            if room_options:
                room = random.choice(room_options)
                timeslot = random.choice(TIMESLOTS)
                teacher = course.get('teacher', 'Unknown')  # Get teacher or default to 'Unknown'
                individual.append({
                    'course': course['name'],
                    'room': room,
                    'timeslot': timeslot,
                    'teacher': teacher
                })
        else:
            print(f"Invalid course entry: {course}")  # Debugging line to identify bad data
    return individual


def generate_initial_population_with_cp(population_size=50):
    population = []
    attempts = 0
    
    while len(population) < population_size and attempts < 2 * population_size:
        individual = generate_individual()
        if individual:  # Only add fully valid individuals
            population.append(individual)
        attempts += 1
    
    # Log and return final population
    if population:
        logging.info("Generated Population Sample: " + str(population[0]))
    else:
        logging.warning("No valid population could be generated with the given constraints.")
    
    return population

