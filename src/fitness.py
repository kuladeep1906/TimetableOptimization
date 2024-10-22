from data.input_data import TIMESLOTS,TEACHERS
# Example of teacher preferences 
teacher_preferences = {
    "Mr. A": "9 AM",  # Mr. A prefers 9 AM
    "Ms. B": "11 AM", # Ms. B prefers 11 AM
    "Mr. C": "10 AM", # Mr. C prefers 10 AM
    # Add preferences for other teachers
}

# Define room preferences for certain courses
room_preferences = {
    "Chemistry": "Room 2",  # Chemistry must be assigned to Room 2 (Science Lab)
    "Physics": "Room 1",    # Physics prefers Room 1
    # Add more preferences as needed
}

# Define Teacher-Course Pairings
teacher_course_pairings = {
    "Math": "Mr. A",     # Mr. A must always teach Math
    "Physics": "Ms. B",  # Ms. B must always teach Physics
    "Chemistry": "Mr. C",  # Mr. C must always teach Chemistry
    "History": "Mr. D",   # Mr. D must always teach History
    "English": "Ms. E"    # Ms. E must always teach English
}


def evaluate(timetable):
    """
    Fitness function to evaluate the timetable based on room conflicts, teacher conflicts,
    teacher preferences, workload optimization, room preferences, and course distribution balance.
    """
    fitness = 0
    max_courses_per_teacher = 3  # Define the maximum number of courses a teacher can handle per day
    room_usage = {timeslot: [] for timeslot in TIMESLOTS}
    teacher_usage = {timeslot: [] for timeslot in TIMESLOTS}
    teacher_course_count = {teacher['name']: 0 for teacher in TEACHERS}
    timeslot_distribution = {timeslot: 0 for timeslot in TIMESLOTS}

    for course, room, teacher, timeslot in timetable:
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
        if course in room_preferences and room_preferences[course] != room:
            fitness -= 5  # Penalty for not assigning course to preferred room

        # Track how many courses are scheduled in each timeslot
        timeslot_distribution[timeslot] += 1

         # Teacher-Course Pairing Check
        if course in teacher_course_pairings and teacher_course_pairings[course] != teacher:
            fitness -= 10  # Strong penalty if wrong teacher is assigned to the course

    # Soft Constraint: Penalize if too many courses are clustered in the same timeslot
    for timeslot, count in timeslot_distribution.items():
        if count > 3:  # Limit how many courses can be scheduled in the same timeslot
            fitness -= (count - 3) * 5  # Penalize for course clustering

    # Soft Constraint: Penalize overloading a teacher with too many courses
    for teacher, count in teacher_course_count.items():
        if count > max_courses_per_teacher:
            fitness -= (count - max_courses_per_teacher) * 5

    return fitness,
