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
    penalties = {
        'room_capacity': 20,
        'teacher_availability': 10,
        'incorrect_teacher': 15,
        'max_courses': 25,
        'consecutive_classes': 8,
        'timeslot_conflict': 20,
        'program_overlap': 30,
        'prerequisite_order': 25,
    }
    bonuses = {
        'preferred_room': 5,
        'primary_preferred_room': 10,
        'preferred_timeslot': 7,
        'teacher_efficiency': 5,
        'room_distribution': 3,
    }
    max_courses_per_teacher = 3

    teacher_course_count = Counter()
    teacher_timeslots = defaultdict(list)
    room_timeslots = defaultdict(list)
    room_program_timeslot = defaultdict(list)

    for entry in timetable:
        course = next(course for course in COURSES if course['name'] == entry['course'])
        room = next(room for room in ROOMS if room['name'] == entry['room'])
        teacher = next(teacher for teacher in TEACHERS if teacher['name'] == entry['teacher'])

        # HARD: Room capacity must not be exceeded
        if course['students'] > room['capacity']:
            score -= penalties['room_capacity']

        # HARD: Teacher availability constraint
        if entry['timeslot'] not in teacher['availability']:
            score -= penalties['teacher_availability']

        # HARD: Teacher must teach their assigned course
        if entry['teacher'] != course['teacher']:
            score -= penalties['incorrect_teacher']

        # SOFT: Reward if the assigned room matches the course's preferred rooms
        if entry['room'] in course['preferred_rooms']:
            score += bonuses['preferred_room']
            if entry['room'] == course['preferred_rooms'][0]:
                score += bonuses['primary_preferred_room']

        # SOFT: Reward preferred timeslot for teachers
        if 'preferred_timeslots' in teacher and entry['timeslot'] in teacher['preferred_timeslots']:
            score += bonuses['preferred_timeslot']

        # Update counters for global constraints
        teacher_course_count[entry['teacher']] += 1
        parsed_timeslot = parse_timeslot(entry['timeslot'])
        if parsed_timeslot != -1:
            teacher_timeslots[entry['teacher']].append(parsed_timeslot)
            room_timeslots[entry['room']].append(parsed_timeslot)

        # Track programs in the same room and timeslot for overlap checking
        if 'program' in course:
            room_program_timeslot[(entry['room'], entry['timeslot'])].append(course['program'])

    # HARD: Teacher must not exceed the maximum number of courses allowed
    for teacher, count in teacher_course_count.items():
        if count > max_courses_per_teacher:
            score -= (count - max_courses_per_teacher) * penalties['max_courses']

    # SOFT: Penalize consecutive classes for teachers
    for teacher, timeslots in teacher_timeslots.items():
        timeslots.sort()
        for i in range(1, len(timeslots)):
            if timeslots[i] == timeslots[i - 1] + 1:
                score -= penalties['consecutive_classes']

    # HARD: Avoid overlapping timeslots for the same teacher or room
    for timeslot_list in teacher_timeslots.values():
        if len(timeslot_list) != len(set(timeslot_list)):
            score -= penalties['timeslot_conflict']

    for timeslot_list in room_timeslots.values():
        if len(timeslot_list) != len(set(timeslot_list)):
            score -= penalties['timeslot_conflict']

    # HARD: Avoid overlapping programs in the same room and timeslot
    for key, programs in room_program_timeslot.items():
        if len(programs) != len(set(programs)):
            score -= penalties['program_overlap']

    # HARD: Ensure courses with prerequisites are scheduled in the correct order
    course_times = {entry['course']: entry['timeslot'] for entry in timetable}
    for course in COURSES:
        if 'prerequisite' in course and course['prerequisite'] in course_times:
            prerequisite_time = parse_timeslot(course_times[course['prerequisite']])
            course_time = parse_timeslot(course_times[course['name']])
            if prerequisite_time >= course_time:
                score -= penalties['prerequisite_order']

    # SOFT: Reward teachers who handle more than the average number of courses
    average_courses = sum(teacher_course_count.values()) / len(TEACHERS)
    for teacher, count in teacher_course_count.items():
        if count > average_courses:
            score += (count - average_courses) * bonuses['teacher_efficiency']

    # SOFT: Reward balanced room distribution
    room_usage = Counter(entry['room'] for entry in timetable)
    ideal_usage = len(COURSES) / len(ROOMS)  # Target is even distribution
    for room_name, usage in room_usage.items():
        score -= abs(usage - ideal_usage) * bonuses['room_distribution']

    return max(0, score)  # Ensure fitness score is never negative
