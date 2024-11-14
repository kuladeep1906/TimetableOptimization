import logging
import os
import time
from .genetic_algorithm import genetic_algorithm
from .rta_star import rta_star_algorithm
from .simulated_annealing import simulated_annealing
from .hill_climbing import hill_climbing
from .tabu_search import tabu_search

# Ensure the logs folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Clear the log files at the start of each run
with open("logs/detailed_logs.log", "w") as f:
    f.write("")  # Clears detailed_logs.log
with open("logs/final_output.log", "w") as f:
    f.write("")  # Clears final_output.log

# Set up logging for detailed logs
logging.basicConfig(
    filename="logs/detailed_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger()

# Set up logger for final output
final_output_logger = logging.getLogger("final_output")
final_output_logger.setLevel(logging.INFO)
final_output_handler = logging.FileHandler("logs/final_output.log")
final_output_handler.setFormatter(logging.Formatter("%(message)s"))
final_output_logger.addHandler(final_output_handler)

def main(algorithm_choice=None):
    # If algorithm_choice is None, prompt the user for input
    if algorithm_choice is None:
        print("Choose an option:")
        print("1. Run Genetic Algorithm")
        print("2. Run RTA* Algorithm")
        print("3. Run Simulated Annealing")
        print("4. Run Hill Climbing")
        print("5. Run Tabu Search")
        print("6. Choose the optimal timetable from all algorithms")
        algorithm_choice = input("Enter your choice (1/2/3/4/5/6): ")

    output_file = "optimal_timetable_output.txt"
    algorithm_used = "Unknown Algorithm"  # Default initialization
    best_schedule = []
    best_fitness = 0
    elapsed_time = None

    if algorithm_choice == '1':
        logger.info("\n--- Starting Genetic Algorithm ---\n")
        best_schedule, best_fitness, elapsed_time = genetic_algorithm(logger)
        algorithm_used = "Genetic Algorithm"
        logger.info("\n--- Genetic Algorithm Ended ---\n")
        
    elif algorithm_choice == '2':
        logger.info("\n--- Starting RTA* Algorithm ---\n")
        best_schedule, best_fitness, elapsed_time = rta_star_algorithm(logger)
        algorithm_used = "RTA* Algorithm"
        logger.info("\n--- RTA* Algorithm Ended ---\n")

    elif algorithm_choice == '3':
        logger.info("\n--- Starting Simulated Annealing ---\n")
        best_schedule, best_fitness, elapsed_time = simulated_annealing(logger)
        algorithm_used = "Simulated Annealing"
        logger.info("\n--- Simulated Annealing Ended ---\n")

    elif algorithm_choice == '4':
        logger.info("\n--- Starting Hill Climbing ---\n")
        best_schedule, best_fitness, elapsed_time = hill_climbing(logger)
        algorithm_used = "Hill Climbing"
        logger.info("\n--- Hill Climbing Ended ---\n")
        
    elif algorithm_choice == '5':
        logger.info("\n--- Starting Tabu Search ---\n")
        best_schedule, best_fitness, elapsed_time = tabu_search(logger)
        algorithm_used = "Tabu Search"
        logger.info("\n--- Tabu Search Ended ---\n")

    elif algorithm_choice == '6':
        logger.info("\n--- Starting All Algorithms for Comparison ---\n")

        # Clear final_output.log once at the beginning
        with open("logs/final_output.log", "w") as log_file:
            log_file.write("All Algorithms - Final Comparison Results\n")

        # Start timing the entire comparison process
        comparison_start_time = time.time()
        
        # Run each algorithm and log final results for comparison
        algorithms = [
            ("Genetic Algorithm", genetic_algorithm),
            ("RTA* Algorithm", rta_star_algorithm),
            ("Simulated Annealing", simulated_annealing),
            ("Hill Climbing", hill_climbing),
            ("Tabu Search", tabu_search)
        ]
        
        all_schedules = []
        
        for algo_name, algo_func in algorithms:
            logger.info(f"\n--- Starting {algo_name} ---\n")
            best_schedule, best_fitness, elapsed_time = algo_func(logger)
            all_schedules.append((algo_name, best_schedule, best_fitness, elapsed_time))
            
            # Log each algorithm's final result in a consistent format
            with open("logs/final_output.log", "a") as log_file:
                log_file.write(f"\n{algo_name} - Final Results\n")
                log_file.write(f"Best Fitness: {best_fitness}\n")
                log_file.write(f"Time Taken: {elapsed_time:.2f} seconds\n")
                log_file.write("Best Timetable Configuration:\n")
                for entry in best_schedule:
                    log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}\n")

        logger.info("\n--- All Algorithms for Comparison Ended ---\n")

        # Calculate total elapsed time for running all algorithms
        comparison_end_time = time.time()
        total_comparison_time = comparison_end_time - comparison_start_time

        # Determine the best algorithm based on fitness score (higher is better)
        best_algorithm, best_schedule, best_fitness, best_time = max(all_schedules, key=lambda x: (x[2], -x[3]))

        # Log the best algorithm and timetable configuration to final_output.log
        with open("logs/final_output.log", "a") as log_file:
            log_file.write("\n--- Best Algorithm ---\n")
            log_file.write(f"Best Algorithm: {best_algorithm}\n")
            log_file.write(f"Best Fitness: {best_fitness}\n")
            log_file.write(f"Time Taken: {best_time:.2f} seconds\n")
            log_file.write("Best Timetable Configuration:\n")
            for entry in best_schedule:
                log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}\n")
        
        # Log total time taken for comparison
        with open("logs/final_output.log", "a") as log_file:
            log_file.write("\n--- Total Comparison Time ---\n")
            log_file.write(f"Total Time Taken to Compare All Algorithms: {total_comparison_time:.2f} seconds\n")

    
   
   
   
   
   
   
   
   
   
   
   
   
    # Write results to the output file for the selected algorithm
    with open(output_file, "w") as file:
        file.write(f"Results from {algorithm_used}:\n")
        file.write("Best Timetable Configuration:\n")
        for entry in best_schedule:
            file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}\n")
        file.write(f"\nFitness Score: {best_fitness}\n")
        if elapsed_time:
            file.write(f"Time taken: {elapsed_time:.2f} seconds\n")


if __name__ == "__main__":
    main()
