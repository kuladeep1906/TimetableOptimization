from data.input_data import COURSES, TEACHERS, ROOMS
from collections import Counter, defaultdict

# Helper function to convert timeslot strings to integers
def parse_timeslot(timeslot):
    time_mapping = {
        '9 AM': 9, '10 AM': 10, '11 AM': 11, '12 PM': 12,
        '1 PM': 13, '2 PM': 14, '3 PM': 15, '4 PM': 16,
        '5 PM': 17, '6 PM': 18
    }
    return time_mapping.get(timeslot, -1)  # Returns -1 if timeslot is invalid

def calculate_fitness(timetable):
    score = 0
    # Define penalties and bonuses
    room_capacity_penalty = 20
    teacher_availability_penalty = 10
    preferred_room_bonus = 5
    primary_preferred_room_bonus = 10
    incorrect_teacher_penalty = 15
    max_courses_penalty = 25
    max_courses_per_teacher = 3
    consecutive_classes_penalty = 8
    timeslot_conflict_penalty = 20

    teacher_course_count = Counter()
    teacher_timeslots = defaultdict(list)
    room_timeslots = defaultdict(list)

    for entry in timetable:
        course = next(course for course in COURSES if course['name'] == entry['course'])
        room = next(room for room in ROOMS if room['name'] == entry['room'])
        
        # Penalize if room capacity is exceeded
        if course['students'] > room['capacity']:
            score -= room_capacity_penalty

        # Penalize if the course is not assigned to the specified teacher
        if entry['teacher'] != course['teacher']:
            score -= incorrect_teacher_penalty

        # Track the number of courses assigned to each teacher
        teacher_course_count[entry['teacher']] += 1

        # Track the timeslot assignment for this teacher and room, using parsed integer timeslots
        parsed_timeslot = parse_timeslot(entry['timeslot'])
        if parsed_timeslot != -1:  # Only add valid parsed timeslots
            teacher_timeslots[entry['teacher']].append(parsed_timeslot)
            room_timeslots[entry['room']].append(parsed_timeslot)

        # Penalize if timeslot does not match teacher availability
        teacher = next(teacher for teacher in TEACHERS if teacher['name'] == entry['teacher'])
        if entry['timeslot'] not in teacher['availability']:
            score -= teacher_availability_penalty

        # Reward if the assigned room matches the course's preferred rooms
        if entry['room'] in course['preferred_rooms']:
            score += preferred_room_bonus
            if entry['room'] == course['preferred_rooms'][0]:
                score += primary_preferred_room_bonus

    # Penalize if a teacher is assigned more than the maximum courses allowed per day
    for teacher, count in teacher_course_count.items():
        if count > max_courses_per_teacher:
            score -= (count - max_courses_per_teacher) * max_courses_penalty

    # Check for consecutive class violations and timeslot conflicts
    for teacher, timeslots in teacher_timeslots.items():
        timeslots.sort()  # Sort parsed timeslots to detect consecutive sessions
        for i in range(1, len(timeslots)):
            if timeslots[i] == timeslots[i - 1] + 1:
                score -= consecutive_classes_penalty

    # Penalize timeslot conflicts within the same room or teacher
    for timeslot_list in teacher_timeslots.values():
        if len(timeslot_list) != len(set(timeslot_list)):
            score -= timeslot_conflict_penalty

    for timeslot_list in room_timeslots.values():
        if len(timeslot_list) != len(set(timeslot_list)):
            score -= timeslot_conflict_penalty

    return score
