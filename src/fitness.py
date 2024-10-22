from data.input_data import COURSES, TEACHERS, TIMESLOTS, ROOMS

def get_preferred_rooms(course_name):
    for course in COURSES:
        if course['name'] == course_name:
            return course['preferred_rooms']
    return []

def get_room_capacity(room_name):
    for room in ROOMS:
        if room['name'] == room_name:
            return room['capacity']
    return 0

def get_course_students(course_name):
    for course in COURSES:
        if course['name'] == course_name:
            return course['students']
    return 0

def evaluate(timetable):
    fitness = 0
    max_courses_per_teacher = 3  # Max number of courses per day
    room_usage = {timeslot: [] for timeslot in TIMESLOTS}
    teacher_usage = {timeslot: [] for timeslot in TIMESLOTS}
    teacher_course_count = {teacher['name']: 0 for teacher in TEACHERS}
    timeslot_distribution = {timeslot: 0 for timeslot in TIMESLOTS}

    # Automatically create teacher-course pairings
    teacher_course_pairings = {course['name']: course['teacher'] for course in COURSES if 'teacher' in course}

    for course, room, teacher, timeslot in timetable:
        course_students = get_course_students(course)
        room_capacity = get_room_capacity(room)

        # Room capacity check (hard constraint)
        if room_capacity < course_students:
            fitness -= 20  # Strong penalty for assigning too many students to a room

        # Room conflict check (hard constraint)
        if room in room_usage[timeslot]:
            fitness -= 10
        else:
            room_usage[timeslot].append(room)

        # Teacher conflict check (hard constraint)
        if teacher in teacher_usage[timeslot]:
            fitness -= 10
        else:
            teacher_usage[timeslot].append(teacher)

        # Track the number of courses assigned to each teacher
        teacher_course_count[teacher] += 1

        # Soft Constraint: Penalize if course is not scheduled in preferred room
        preferred_rooms = get_preferred_rooms(course)
        if preferred_rooms and room not in preferred_rooms:
            fitness -= 5

        # Track how many courses are scheduled in each timeslot
        timeslot_distribution[timeslot] += 1

        # Teacher-Course Pairing Check
        if course in teacher_course_pairings and teacher_course_pairings[course] != teacher:
            fitness -= 10

    # Soft Constraint: Penalize if too many courses are clustered in the same timeslot
    for timeslot, count in timeslot_distribution.items():
        if count > 3:
            fitness -= (count - 3) * 5

    # Soft Constraint: Penalize overloading a teacher with too many courses
    for teacher, count in teacher_course_count.items():
        if count > max_courses_per_teacher:
            fitness -= (count - max_courses_per_teacher) * 5

    return fitness,
