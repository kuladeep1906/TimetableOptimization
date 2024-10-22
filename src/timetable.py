import random
from data.input_data import COURSES, ROOMS, TEACHERS, TIMESLOTS  # Import data

class Timetable:
    def __init__(self, existing_timetable=None):
        """
        Initialize timetable either from an existing solution (for RTA*) or create a random solution.
        """
        self.timetable = []

        if existing_timetable:  # For RTA*, when refining an existing timetable
            self.timetable = existing_timetable
        else:  # Create a random timetable
            for course in COURSES:
                room = random.choice([r['name'] for r in ROOMS if r['capacity'] >= course['students']])

                # Select a teacher and make sure they are available for the timeslot
                teacher = random.choice(TEACHERS)
                available_timeslots = teacher['availability']
                if not available_timeslots:
                    raise ValueError(f"No available timeslots for teacher {teacher['name']}")
                
                timeslot = random.choice(available_timeslots)

                # Append course, room, teacher, and timeslot to the timetable
                self.timetable.append((course['name'], room, teacher['name'], timeslot))

    def __str__(self):
        """
        Print the timetable in a readable format.
        """
        result = ""
        for course, room, teacher, timeslot in self.timetable:
            result += f"Course: {course}, Room: {room}, Teacher: {teacher}, Timeslot: {timeslot}\n"
        return result

    def mutate(self, indpb=0.1):
        """
        Perform mutation by changing room, teacher, or timeslot randomly.
        """
        for i in range(len(self.timetable)):
            if random.random() < indpb:
                course, _, _, _ = self.timetable[i]

                # Mutate room
                room = random.choice([r['name'] for r in ROOMS if r['capacity'] >= COURSES[i]['students']])

                # Mutate teacher
                teacher = random.choice(TEACHERS)
                available_timeslots = teacher['availability']
                if not available_timeslots:
                    raise ValueError(f"No available timeslots for teacher {teacher['name']}")
                
                # Mutate timeslot
                timeslot = random.choice(available_timeslots)

                self.timetable[i] = (course, room, teacher['name'], timeslot)

    def get_timetable_entries(self):
        """
        Return the internal timetable entries for evaluation.
        """
        return self.timetable
