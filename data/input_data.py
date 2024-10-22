# data/input_data.py
COURSES = [
    {'name': 'Math', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 2']},
    {'name': 'Physics', 'students': 30, 'preferred_rooms': ['Room 2']},
    {'name': 'Business Analytics', 'students': 25, 'preferred_rooms': ['Room 3']},
    {'name': 'Computer Science', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 3']},
    {'name': 'English', 'students': 35, 'preferred_rooms': ['Room 1']}
]

TEACHERS = [
    {'name': 'Mr. A', 'availability': ['9 AM', '10 AM', '11 AM']},
    {'name': 'Ms. B', 'availability': ['10 AM', '11 AM', '12 PM']},
    {'name': 'Mr. C', 'availability': ['9 AM', '12 PM', '1 PM']},
    {'name': 'Ms. D', 'availability': ['9 AM', '10 AM', '1 PM']},
    {'name': 'Mr. E', 'availability': ['11 AM', '12 PM', '1 PM']}
]

ROOMS = [
    {'name': 'Room 1', 'capacity': 30},
    {'name': 'Room 2', 'capacity': 30},
    {'name': 'Room 3', 'capacity': 30},
    {'name': 'Room 3', 'capacity': 40}
]

TIMESLOTS = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM']
