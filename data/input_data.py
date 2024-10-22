COURSES = [
    {'name': 'Advanced Data Analytics', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 2'], 'teacher': 'Mr. A'},
    {'name': 'Artificial Intelligence', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 2'], 'teacher': 'Mr. A'},
    {'name': 'Business Analytics', 'students': 25, 'preferred_rooms': ['Room 3'], 'teacher': 'Ms. B'},
    {'name': 'Computer Science', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 3'], 'teacher': 'Mr. C'},  # Mr. C can teach Computer Science & Cyber Security
    {'name': 'Cyber Security', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 3'], 'teacher': 'Mr. C'},
    {'name': 'Data Science', 'students': 30, 'preferred_rooms': ['Room 2'], 'teacher': 'Ms. D'},
    {'name': 'Data Mining Machine Learning', 'students': 30, 'preferred_rooms': ['Room 2'], 'teacher': 'Ms. D'},
    {'name': 'Big Data Analytics', 'students': 30, 'preferred_rooms': ['Room 1,2,4'], 'teacher': 'Mr. E'}, 
    {'name': 'Heuristic Search', 'students': 35, 'preferred_rooms': ['Room 4'], 'teacher': 'Mr. E'},
    {'name': 'Real Time Systems', 'students': 35, 'preferred_rooms': ['Room 4'], 'teacher': 'Mr. E'},
    {'name': 'Reinforcement Learning', 'students': 35, 'preferred_rooms': ['Room 1,5'], 'teacher': 'Mr. F'},
    {'name': 'Machine Learning Design', 'students': 35, 'preferred_rooms': ['Room 4,5'], 'teacher': 'Mr. F'},
    {'name': 'Cloud Computing', 'students': 40, 'preferred_rooms': ['Room 3,5'], 'teacher': 'Mr. G'},
    {'name': 'Computer Networking', 'students': 40, 'preferred_rooms': ['Room 1,5'], 'teacher': 'Mr. G'}
    
   
]


TEACHERS = [
    {'name': 'Mr. A', 'availability': ['9 AM', '10 AM', '11 AM']},
    {'name': 'Ms. B', 'availability': ['10 AM', '11 AM', '12 PM']},
    {'name': 'Mr. C', 'availability': ['9 AM', '12 PM', '1 PM']},
    {'name': 'Ms. D', 'availability': ['9 AM', '10 AM', '1 PM']},
    {'name': 'Mr. E', 'availability': ['11 AM', '12 PM', '1 PM']},
    {'name': 'Mr. F', 'availability': ['9 AM', '12 PM', '1 PM']},
    {'name': 'Mr. G', 'availability': ['10 AM', '11 AM', '1 PM']}
]

ROOMS = [
    {'name': 'Room 1', 'capacity': 30},
    {'name': 'Room 2', 'capacity': 30},
    {'name': 'Room 3', 'capacity': 30},
    {'name': 'Room 4', 'capacity': 40},
    {'name': 'Room 5', 'capacity': 35}
]

TIMESLOTS = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM']
