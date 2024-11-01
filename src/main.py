import logging
import os
from datetime import datetime
from src.constraint_programming import generate_initial_population_with_cp
from src.genetic_algorithm import run_genetic_algorithm
from src.simulated_annealing import run_simulated_annealing
from src.tabu_search import run_tabu_search
from src.rta_star import refine_with_rta_star

# Ensure directories for logs and outputs exist
os.makedirs('logs/timetable_optimization', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# Define log file and final output file paths
log_file = f'logs/timetable_optimization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
final_output_file = 'output/final_output.txt'

# Set up logging configuration with the log file handler
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
file_handler = logging.FileHandler(log_file, mode='a')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(message)s'))
logging.getLogger().addHandler(file_handler)

def clean_old_logs(log_dir='logs/', keep=3):
    """Keeps only the last `keep` log files, deletes the older ones."""
    log_files = sorted(
        [f for f in os.listdir(log_dir) if f.startswith("timetable_optimization_")],
        key=lambda x: os.path.getmtime(os.path.join(log_dir, x))
    )
    if len(log_files) > keep:
        for old_log in log_files[:-keep]:
            try:
                os.remove(os.path.join(log_dir, old_log))
                print(f"Deleted old log file: {old_log}")
            except Exception as e:
                print(f"Error deleting file {old_log}: {e}")

def main():
    # Step 1: Generate initial population using constraint programming
    initial_population = generate_initial_population_with_cp()
    logging.info("Initial population generated with constraint programming.")

    # Step 2: Optimize initial population with Genetic Algorithm
    best_solution = run_genetic_algorithm(initial_population)
    logging.info("Best solution after Genetic Algorithm:")
    logging.info(str(best_solution))

    # Step 3: Refine solution using Simulated Annealing
    annealed_solution = run_simulated_annealing(best_solution, max_iterations=50, initial_temp=100, cooling_rate=0.9)
    logging.info("Solution refined with Simulated Annealing:")
    logging.info(str(annealed_solution))

    # Step 4: Further refine solution with RTA*
    refined_solution = refine_with_rta_star(annealed_solution)
    logging.info("Solution refined with RTA*:")
    logging.info(str(refined_solution))

    # Step 5: Final optimization using Tabu Search
    final_solution = run_tabu_search(refined_solution)
    logging.info("Final optimized solution after Tabu Search:")
    
    # Log and store the final output in final_output_file
    with open(final_output_file, 'w') as f_out:
        logging.info("Final Optimized Timetable:")
        for entry in final_solution:
            log_entry = f"Course: {entry['course']}, Room: {entry['room']}, Timeslot: {entry['timeslot']}, Teacher: {entry['teacher']}"
            logging.info(log_entry)
            f_out.write(log_entry + '\n')
    
    # Clean up old log files
    clean_old_logs()

if __name__ == "__main__":
    main()
