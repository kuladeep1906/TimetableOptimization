COURSES = [
    {'name': 'Advanced Data Analytics', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 2'], 'teacher': 'Mr. A'},
    {'name': 'Artificial Intelligence', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 2'], 'teacher': 'Mr. A'},
    {'name': 'Business Analytics', 'students': 25, 'preferred_rooms': ['Room 3'], 'teacher': 'Ms. B'},
    {'name': 'Computer Science', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 3'], 'teacher': 'Mr. C'},
    {'name': 'Cyber Security', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 3'], 'teacher': 'Mr. C'},
    {'name': 'Data Science', 'students': 30, 'preferred_rooms': ['Room 2'], 'teacher': 'Ms. D'},
    {'name': 'Data Mining & Machine Learning', 'students': 30, 'preferred_rooms': ['Room 2'], 'teacher': 'Ms. D'},
    {'name': 'Big Data Analytics', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 2', 'Room 4'], 'teacher': 'Mr. E'},
    {'name': 'Heuristic Search', 'students': 35, 'preferred_rooms': ['Room 4'], 'teacher': 'Mr. E'},
 '''   {'name': 'Real-Time Systems', 'students': 35, 'preferred_rooms': ['Room 4'], 'teacher': 'Mr. E'},
    {'name': 'Reinforcement Learning', 'students': 35, 'preferred_rooms': ['Room 1', 'Room 5'], 'teacher': 'Mr. F'},
    {'name': 'Machine Learning Design', 'students': 35, 'preferred_rooms': ['Room 4', 'Room 5'], 'teacher': 'Mr. F'},
    {'name': 'Cloud Computing', 'students': 40, 'preferred_rooms': ['Room 3', 'Room 5'], 'teacher': 'Mr. G'},
    {'name': 'Computer Networking', 'students': 40, 'preferred_rooms': ['Room 1', 'Room 5'], 'teacher': 'Mr. G'},
    {'name': 'Operating Systems', 'students': 30, 'preferred_rooms': ['Room 2'], 'teacher': 'Ms. H'},
    {'name': 'Database Systems', 'students': 30, 'preferred_rooms': ['Room 3'], 'teacher': 'Ms. I'},
    {'name': 'Embedded Systems', 'students': 35, 'preferred_rooms': ['Room 4'], 'teacher': 'Mr. J'},
    {'name': 'Software Engineering', 'students': 35, 'preferred_rooms': ['Room 1'], 'teacher': 'Ms. K'},
    {'name': 'Web Development', 'students': 30, 'preferred_rooms': ['Room 2', 'Room 3'], 'teacher': 'Ms. L'},
    {'name': 'Mobile Computing', 'students': 35, 'preferred_rooms': ['Room 4', 'Room 5'], 'teacher': 'Mr. M'},
    {'name': 'Image Processing', 'students': 30, 'preferred_rooms': ['Room 3'], 'teacher': 'Ms. N'},
    {'name': 'Signal Processing', 'students': 30, 'preferred_rooms': ['Room 2'], 'teacher': 'Mr. O'},
    {'name': 'Natural Language Processing', 'students': 35, 'preferred_rooms': ['Room 5'], 'teacher': 'Mr. P'},
    {'name': 'Deep Learning', 'students': 40, 'preferred_rooms': ['Room 1', 'Room 5'], 'teacher': 'Mr. A'},
    {'name': 'Robotics', 'students': 40, 'preferred_rooms': ['Room 1', 'Room 4'], 'teacher': 'Ms. B'},
    {'name': 'Quantum Computing', 'students': 30, 'preferred_rooms': ['Room 2', 'Room 3'], 'teacher': 'Mr. C'},
    {'name': 'Internet of Things', 'students': 35, 'preferred_rooms': ['Room 4'], 'teacher': 'Mr. D'},
    {'name': 'Augmented Reality', 'students': 35, 'preferred_rooms': ['Room 3'], 'teacher': 'Mr. E'},
    {'name': 'Virtual Reality', 'students': 30, 'preferred_rooms': ['Room 2'], 'teacher': 'Ms. F'},
    {'name': 'Blockchain Technology', 'students': 30, 'preferred_rooms': ['Room 3', 'Room 5'], 'teacher': 'Mr. G'},
    {'name': 'Ethics in AI', 'students': 25, 'preferred_rooms': ['Room 1'], 'teacher': 'Ms. H'},
    {'name': 'Digital Signal Processing', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 3','Room 7'], 'teacher': 'Mr. I'},
    {'name': 'High-Performance Computing', 'students': 30, 'preferred_rooms': ['Room 4', 'Room 5'], 'teacher': 'Mr. J'},
    {'name': 'Game Design', 'students': 30, 'preferred_rooms': ['Room 2', 'Room 3'], 'teacher': 'Ms. K'},
    {'name': 'Genetic Algorithms', 'students': 25, 'preferred_rooms': ['Room 1', 'Room 4'], 'teacher': 'Ms. L'},
    {'name': 'Fuzzy Logic', 'students': 35, 'preferred_rooms': ['Room 5'], 'teacher': 'Mr. M'},
    {'name': 'Linear Algebra', 'students': 30, 'preferred_rooms': ['Room 3', 'Room 4'], 'teacher': 'Mr. N'},
    {'name': 'Statistics for AI', 'students': 30, 'preferred_rooms': ['Room 2'], 'teacher': 'Ms. O'},
    {'name': 'Bayesian Inference', 'students': 25, 'preferred_rooms': ['Room 1','Room 6'], 'teacher': 'Mr. P'},
    {'name': 'Data Visualization', 'students': 35, 'preferred_rooms': ['Room 5', 'Room 4'], 'teacher': 'Mr. A'},
    {'name': 'Optimization Techniques', 'students': 40, 'preferred_rooms': ['Room 4','Room 6'], 'teacher': 'Ms. H'},
    {'name': 'Computer Graphics', 'students': 40, 'preferred_rooms': ['Room 7','Room 3', 'Room 5'], 'teacher': 'Mr. I'},
    {'name': 'Software Testing', 'students': 30, 'preferred_rooms': ['Room 2', 'Room 3'], 'teacher': 'Ms. J'},
    {'name': 'Computational Biology', 'students': 35, 'preferred_rooms': ['Room 1','Room 5'], 'teacher': 'Mr. K'},
    {'name': 'Bioinformatics', 'students': 35, 'preferred_rooms': ['Room 4', 'Room 2'], 'teacher': 'Ms. L'},
    {'name': 'Social Network Analysis', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 2'], 'teacher': 'Mr. M'},
    {'name': 'Predictive Analytics', 'students': 30, 'preferred_rooms': ['Room 6','Room 3'], 'teacher': 'Mr. N'},
    {'name': 'Digital Marketing', 'students': 25, 'preferred_rooms': ['Room 2','Room 4'], 'teacher': 'Ms. O'},
    {'name': 'Business Intelligence', 'students': 30, 'preferred_rooms': ['Room 3', 'Room 4'], 'teacher': 'Ms. P'},
    {'name': 'E-commerce', 'students': 30, 'preferred_rooms': ['Room 5''Room 2'], 'teacher': 'Mr. H'}
''']

TEACHERS = [
    {'name': 'Mr. A', 'availability': ['9 AM', '10 AM', '11 AM', '12 PM']},
    {'name': 'Ms. B', 'availability': ['10 AM', '11 AM', '12 PM', '1 PM']},
    {'name': 'Mr. C', 'availability': ['9 AM', '12 PM', '1 PM', '2 PM']},
    {'name': 'Ms. D', 'availability': ['9 AM', '10 AM', '1 PM', '2 PM']},
    {'name': 'Mr. E', 'availability': ['11 AM', '12 PM', '1 PM', '3 PM']},
    {'name': 'Mr. F', 'availability': ['9 AM', '12 PM', '1 PM', '2 PM']},
    {'name': 'Mr. G', 'availability': ['10 AM', '11 AM', '1 PM', '3 PM']},
    {'name': 'Ms. H', 'availability': ['10 AM', '2 PM', '3 PM', '4 PM']},
    {'name': 'Mr. I', 'availability': ['9 AM', '2 PM', '3 PM', '4 PM']},
    {'name': 'Ms. J', 'availability': ['11 AM', '2 PM', '3 PM', '5 PM']},
    {'name': 'Mr. K', 'availability': ['10 AM', '3 PM', '4 PM', '5 PM']},
    {'name': 'Ms. L', 'availability': ['9 AM', '4 PM', '5 PM', '6 PM']},
    {'name': 'Mr. M', 'availability': ['10 AM', '2 PM', '5 PM', '6 PM']},
    {'name': 'Ms. N', 'availability': ['12 PM', '3 PM', '5 PM', '6 PM']},
    {'name': 'Mr. O', 'availability': ['1 PM', '2 PM', '4 PM', '6 PM']},
    {'name': 'Ms. P', 'availability': ['1 PM', '3 PM', '4 PM', '6 PM']},
    
]

ROOMS = [
    {'name': 'Room 1', 'capacity': 30},
    {'name': 'Room 2', 'capacity': 30},
    {'name': 'Room 3', 'capacity': 35},
    {'name': 'Room 4', 'capacity': 40},
    {'name': 'Room 5', 'capacity': 35},
    {'name': 'Room 6', 'capacity': 40},
    {'name': 'Room 7', 'capacity': 50}
]

TIMESLOTS = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM']




'''
import random

# Define a list of 500 courses with random student counts.
COURSES = [
    {"name": f"Course {i}", "students": random.randint(20, 100)} for i in range(3)
]

# Define a list of 26 teachers, each with random availability across different timeslots.
TEACHERS = [
    {
        "name": f"Teacher {chr(65 + i % 26)}",
        "availability": random.sample(["9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"], k=random.randint(2, 5))
    } 
    for i in range(26)
]

# Define a list of 20 rooms with random capacities.
ROOMS = [{"name": f"Room {i + 1}", "capacity": random.randint(30, 150)} for i in range(20)]

# Define a list of available timeslots.
TIMESLOTS = ["9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

# Example course overlap information (courses that share students and should not overlap in times).
course_overlap = {
    "Course 1": ["Course 2", "Course 3"],
    "Course 4": ["Course 5"],
    # Add more as needed.
}

'''
