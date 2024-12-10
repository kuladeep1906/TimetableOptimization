import random
import time
import csv
import os
from data.input_data import COURSES, TEACHERS, ROOMS, TIMESLOTS
from .fitness import parse_timeslot

# Ensure the progress folder exists
if not os.path.exists("progress"):
    os.makedirs("progress")

# Function to initialize CSV log
def initialize_csv_log(algorithm_name):
    """
    Initializes a CSV log file for CSP with static headers.
    """
    csv_path = f"progress/{algorithm_name}_progress.csv"
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write headers relevant to CSP
        writer.writerow(["Course", "Day", "Room", "Timeslot", "Teacher", "Constraint Status"])
    return csv_path

# Function to log CSP progress to CSV
def log_progress_csv(csv_path, course, day, room, timeslot, teacher, status):
    """
    Appends CSP progress to the CSV log.
    """
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([course, day, room, timeslot, teacher, status])  

# Constraint Functions
def room_is_valid(timetable, room, timeslot, day):
    for entry in timetable:
        if entry['room'] == room and entry['timeslot'] == timeslot and entry['day'] == day:
            return False
    return True

def teacher_is_valid(timetable, teacher, timeslot, day):
    for entry in timetable:
        if entry['teacher'] == teacher and entry['timeslot'] == timeslot and entry['day'] == day:
            return False
    return True

def teacher_assigned_correct_course(course, teacher):
    return course['teacher'] == teacher

def avoid_consecutive_classes(timetable, teacher, timeslot, day):
    """
    Checks if the teacher has consecutive classes and enforces a gap.
    """
    for entry in timetable:
        if entry['teacher'] == teacher and entry['day'] == day:
            prev_timeslot = parse_timeslot(entry['timeslot'])
            curr_timeslot = parse_timeslot(timeslot)
            if abs(curr_timeslot - prev_timeslot) == 1: 
                return False
    return True

def duplicate_entry_exists(timetable, course, room, timeslot, day):
    for entry in timetable:
        if entry['course'] == course and entry['room'] == room and entry['timeslot'] == timeslot and entry['day'] == day:
            return True
    return False

def required_instances_met(course, instance_count):
    return instance_count[course["name"]] >= course["instances_per_week"]

def balanced_room_utilization(room_usage, room):
    """
    Ensures rooms are utilized evenly by penalizing overuse of specific rooms.
    """
    return room_usage[room] <= max(room_usage.values()) + 1

def balanced_day_utilization(day_usage, day):
    """
    Ensures days are utilized evenly across the schedule.
    """
    return day_usage[day] <= max(day_usage.values()) + 1

def teacher_preference_satisfied(teacher, day, timeslot):
    """
    Checks if the assigned day and timeslot align with teacher preferences.
    """
    return day in teacher.get("preferred_days", []) and timeslot in teacher.get("preferred_timeslots", TIMESLOTS)


# CSP Backtracking Function with Logging
def solve_scheduling(logger):
    csv_path = initialize_csv_log("CSP")

    def backtrack(timetable, course_index, instance_count, room_usage, day_usage):
        if course_index == len(COURSES):
            logger.info("All courses have been successfully scheduled.")
            return timetable

        course = COURSES[course_index]
        remaining_instances = course["instances_per_week"] - instance_count[course["name"]]
        logger.info(f"Scheduling Course: {course['name']} | Remaining Instances: {remaining_instances}")

        if remaining_instances == 0:
            return backtrack(timetable, course_index + 1, instance_count, room_usage, day_usage)

        # Randomize days and times to encourage broader utilization
        random_days = random.sample(TEACHERS[course_index % len(TEACHERS)]["preferred_days"], len(TEACHERS[course_index % len(TEACHERS)]["preferred_days"]))
        random_timeslots = random.sample(TIMESLOTS, len(TIMESLOTS))

        for day in random_days:
            for timeslot in random_timeslots:
                for room in course["preferred_rooms"]:
                    teacher = course["teacher"]

                    logger.debug(f"Attempting to schedule: {course['name']} | Day: {day} | Timeslot: {timeslot} | Room: {room} | Teacher: {teacher}")

                    # Check all constraints
                    if duplicate_entry_exists(timetable, course["name"], room, timeslot, day):
                        log_progress_csv(csv_path, course['name'], day, room, timeslot, teacher, "Duplicate Entry")
                        logger.warning(f"Constraint Violated: Duplicate Entry for {course['name']} at {timeslot} on {day} in {room}")
                        continue
                    if not room_is_valid(timetable, room, timeslot, day):
                        log_progress_csv(csv_path, course['name'], day, room, timeslot, teacher, "Room Conflict")
                        logger.warning(f"Constraint Violated: Room Conflict for {course['name']} at {timeslot} on {day} in {room}")
                        continue
                    if not teacher_is_valid(timetable, teacher, timeslot, day):
                        log_progress_csv(csv_path, course['name'], day, room, timeslot, teacher, "Teacher Conflict")
                        logger.warning(f"Constraint Violated: Teacher Conflict for {teacher} at {timeslot} on {day}")
                        continue
                    if not teacher_assigned_correct_course(course, teacher):
                        log_progress_csv(csv_path, course['name'], day, room, timeslot, teacher, "Wrong Assignment")
                        logger.warning(f"Constraint Violated: Teacher {teacher} is not assigned to {course['name']}")
                        continue
                    if not avoid_consecutive_classes(timetable, teacher, timeslot, day):
                        log_progress_csv(csv_path, course['name'], day, room, timeslot, teacher, "Consecutive Classes Conflict")
                        logger.warning(f"Constraint Violated: Consecutive Classes for {teacher} on {day}")
                        continue
                    if not balanced_room_utilization(room_usage, room):
                        log_progress_csv(csv_path, course['name'], day, room, timeslot, teacher, "Room Overuse")
                        logger.warning(f"Constraint Violated: Room Overuse for {room}")
                        continue
                    if not balanced_day_utilization(day_usage, day):
                        log_progress_csv(csv_path, course['name'], day, room, timeslot, teacher, "Day Overuse")
                        logger.warning(f"Constraint Violated: Day Overuse on {day}")
                        continue
                    if not teacher_preference_satisfied(TEACHERS[course_index % len(TEACHERS)], day, timeslot):
                        log_progress_csv(csv_path, course['name'], day, room, timeslot, teacher, "Teacher Preference Violation")
                        logger.warning(f"Constraint Violated: Teacher Preference Violation for {teacher} on {day} at {timeslot}")
                        continue

                    # Add to timetable
                    timetable.append({
                        "course": course["name"],
                        "room": room,
                        "teacher": teacher,
                        "timeslot": timeslot,
                        "day": day,
                    })
                    instance_count[course["name"]] += 1
                    room_usage[room] += 1
                    day_usage[day] += 1
                    log_progress_csv(csv_path, course["name"], day, room, timeslot, teacher, "Scheduled")
                    logger.info(f"Scheduled: {course['name']} | Day: {day} | Timeslot: {timeslot} | Room: {room} | Teacher: {teacher}")

                    # Recursive backtrack
                    result = backtrack(
                        timetable,
                        course_index if not required_instances_met(course, instance_count) else course_index + 1,
                        instance_count,
                        room_usage,
                        day_usage
                    )
                    if result:
                        return result

                    # Backtrack
                    timetable.pop()
                    instance_count[course["name"]] -= 1
                    room_usage[room] -= 1
                    day_usage[day] -= 1
                    logger.info(f"Backtracking: Removed {course['name']} | Day: {day} | Timeslot: {timeslot} | Room: {room} | Teacher: {teacher}")

        logger.error(f"Failed to schedule course: {course['name']} after checking all possibilities.")
        return None

    # Initialize solving variables
    start_time = time.time()
    timetable = []
    instance_count = {course["name"]: 0 for course in COURSES}
    room_usage = {room["name"]: 0 for room in ROOMS}  # Track room utilization
    all_days = {day for teacher in TEACHERS for day in teacher["preferred_days"]}
    day_usage = {day: 0 for day in all_days}  # Track day utilization

    logger.info("--- Starting CSP Scheduling ---")
    result = backtrack(timetable, 0, instance_count, room_usage, day_usage)
    elapsed_time = time.time() - start_time

    if result:
        logger.info("Final Timetable Configuration (CSP):")
        for entry in result:
            logger.info(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}")
    else:
        logger.error("No valid timetable could be found.")

    logger.info(f"Total Time Elapsed: {elapsed_time:.2f} seconds")
    return result, len(result) if result else 0, elapsed_time, csv_path
