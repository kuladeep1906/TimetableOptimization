from data.input_data import ROOMS, TEACHERS, COURSES, TIMESLOTS

def get_preferred_rooms(course_name):
    for course in COURSES:
        if isinstance(course, dict) and course.get('name') == course_name:
            return course.get('preferred_rooms', [])
    return []

def get_room_capacity(room_name):
    for room in ROOMS:
        if isinstance(room, dict) and room.get('name') == room_name:
            return room.get('capacity', 0)
    return 0

def get_course_students(course_name):
    for course in COURSES:
        if isinstance(course, dict) and course.get('name') == course_name:
            return course.get('students', 0)
    return 0

def evaluate_fitness(solution):
    if isinstance(solution, dict):  # Wrap in list if single dict
        solution = [solution]

    fitness_score = 0
    max_courses_per_teacher = 3
    room_conflicts = 0
    teacher_conflicts = 0
    capacity_violations = 0
    timeslot_penalties = 0
    preferred_room_penalties = 0
    teacher_course_limit_penalties = 0

    room_usage = {timeslot: [] for timeslot in TIMESLOTS}
    teacher_schedule = {teacher['name']: {timeslot: [] for timeslot in TIMESLOTS} for teacher in TEACHERS if isinstance(teacher, dict)}
    teacher_course_count = {teacher['name']: 0 for teacher in TEACHERS if isinstance(teacher, dict)}
    timeslot_distribution = {timeslot: 0 for timeslot in TIMESLOTS}
    teacher_course_pairings = {course['name']: course['teacher'] for course in COURSES if isinstance(course, dict) and 'teacher' in course}

    print("Evaluating solution structure:", solution)

    for entry in solution:
        if not isinstance(entry, dict) or not all(key in entry for key in ['course', 'room', 'timeslot', 'teacher']):
            print("Invalid entry structure:", entry)
            continue

        course = entry['course']
        room = entry['room']
        timeslot = entry['timeslot']
        teacher = entry['teacher']

        # Retrieve course details
        students = get_course_students(course)

        # Room capacity check
        room_capacity = get_room_capacity(room)
        if room_capacity < students:
            capacity_violations += 20

        # Room conflict check
        if room in room_usage.get(timeslot, []):
            room_conflicts += 10
        else:
            room_usage[timeslot].append(room)

        # Teacher schedule conflict check
        if teacher in teacher_schedule and timeslot in teacher_schedule[teacher]:
            if teacher in teacher_schedule[teacher][timeslot]:
                teacher_conflicts += 10
            else:
                teacher_schedule[teacher][timeslot].append(teacher)

        # Track teacher course count
        teacher_course_count[teacher] += 1

        # Preferred room penalty
        preferred_rooms = get_preferred_rooms(course)
        if preferred_rooms and room not in preferred_rooms:
            preferred_room_penalties += 5

        # Teacher-course pairing penalty
        if course in teacher_course_pairings and teacher_course_pairings[course] != teacher:
            teacher_conflicts += 10

        # Timeslot distribution
        timeslot_distribution[timeslot] += 1

    # Teacher course limit penalty
    for teacher, count in teacher_course_count.items():
        if count > max_courses_per_teacher:
            teacher_course_limit_penalties += (count - max_courses_per_teacher) * 5

    # Timeslot overuse penalty
    for timeslot, count in timeslot_distribution.items():
        if count > 3:
            timeslot_penalties += (count - 3) * 5

    # Calculate total fitness score
    fitness_score = (room_conflicts + teacher_conflicts + capacity_violations +
                     preferred_room_penalties + teacher_course_limit_penalties + timeslot_penalties)
    print(f"Fitness Score: {fitness_score}")
    return fitness_score
