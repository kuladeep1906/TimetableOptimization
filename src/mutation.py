from deap import creator
from src.timetable import Timetable

def mutate_timetable(individual, indpb=0.1):
    """
    Mutate the timetable by changing room, teacher, or timeslot randomly for some courses.
    The result should still be an instance of creator.Individual.
    """
    # Mutate the individual by creating a new Timetable
    mutated_timetable = Timetable()
    mutated_timetable.mutate(indpb=indpb)
    
    # Return the mutated timetable as a creator.Individual
    new_individual = creator.Individual(mutated_timetable.timetable)
    return new_individual,
