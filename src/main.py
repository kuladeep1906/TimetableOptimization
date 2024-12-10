import logging
import os
import time
import matplotlib.pyplot as plt  
from .genetic_algorithm import genetic_algorithm
from .a_star import a_star_algorithm
from .simulated_annealing import simulated_annealing
from .hill_climbing import hill_climbing
from .tabu_search import tabu_search
from .csp import solve_scheduling

import pandas as pd  
import numpy as np 

# Ensure the logs folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Ensure the progress CSV folder exists
if not os.path.exists("progress"):
    os.makedirs("progress")

# Clear the log files at the start of each run
with open("logs/detailed_logs.log", "w") as f:
    f.write("")  
with open("logs/final_output.log", "w") as f:
    f.write("") 

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

def plot_progress(csv_path, algorithm_name):
    """
    Plots the progress of fitness scores over generations for a given algorithm.
    """
    # Ensure the progress directory exists
    STATIC_DIR = "static"
    progress_dir = os.path.join(STATIC_DIR, "progress")
    os.makedirs(progress_dir, exist_ok=True)

    try:
        # Read data from the CSV file
        data = pd.read_csv(csv_path)

        # Check for required columns
        required_columns = {'Generation', 'Overall Best Fitness', 'Current Best Fitness'}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"CSV file is missing required columns: {required_columns - set(data.columns)}")

        # Plot progress
       
        plt.plot(
            data['Generation'], 
            data['Current Best Fitness'],  
            color='green',  
            linestyle='--', 
            marker='x'
        )
        
        plt.xlabel("Generation", fontsize=14)
        plt.ylabel("Fitness", fontsize=14)
        plt.title(f"Algorithm Progress for {algorithm_name}", fontsize=16, fontweight='bold')
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.gcf().subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9)

        # Construct output path
        sanitized_name = algorithm_name.replace(' ', '_').replace('*', 'star').lower()
        output_path = os.path.join(progress_dir, f"{sanitized_name}_progress.png")
        
        plt.savefig(output_path)
        plt.close()

        print(f"Progress plot saved to: {output_path}")
        return output_path
    except FileNotFoundError:
        print(f"Error: CSV file not found at path: {csv_path}")
    except ValueError as ve:
        print(f"Error processing CSV file: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def plot_comparison_bar_graph(results):
    """
    Plots a bar graph comparing fitness scores and execution times for all algorithms.
    """
    STATIC_DIR = "static"
    progress_dir = os.path.join(STATIC_DIR, "progress")
    os.makedirs(progress_dir, exist_ok=True)

    try:
        # Extract data
        algo_names = [result[0] for result in results]
        fitness_scores = [result[2] for result in results]
        execution_times = [result[3] for result in results]

        x = np.arange(len(algo_names))  

        # Create bar graph
        fig, ax1 = plt.subplots(figsize=(14, 8))
        bar_width = 0.35

        ax1.bar(x - bar_width/2, fitness_scores, bar_width, label="Fitness Score", color='blue', alpha=0.7)
        ax2 = ax1.twinx()
        ax2.bar(x + bar_width/2, execution_times, bar_width, label="Execution Time (s)", color='orange', alpha=0.7)
        ax1.set_xlabel("Algorithms", fontsize=14)
        ax1.set_ylabel("Fitness Score", fontsize=14, color='blue')
        ax2.set_ylabel("Execution Time (s)", fontsize=14, color='orange')
        ax1.set_title("Comparison of Fitness Scores and Execution Times", fontsize=16, fontweight='bold')

        ax1.set_xticks(x)
        ax1.set_xticklabels(algo_names, fontsize=12)
        ax1.tick_params(axis='y', labelcolor='blue')
        ax2.tick_params(axis='y', labelcolor='orange')

        fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9), fontsize=12)
        fig.tight_layout()

        output_path = os.path.join(progress_dir, "comparison_bar_graph.png")
        plt.savefig(output_path)
        plt.close()

        print(f"Comparison bar graph saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred while creating the comparison bar graph: {e}")

from .csp import solve_scheduling 

def main(algorithm_choice=None):
    if algorithm_choice is None:
        print("Choose an option:")
        print("1. Run CSP")
        print("2. Choose the optimal timetable from all algorithms")
        print("3. Run Genetic Algorithm")
        print("4. Run A* Algorithm")
        print("5. Run Simulated Annealing")
        print("6. Run Hill Climbing")
        print("7. Run Tabu Search")
        
        while True:
            try:
                algorithm_choice = input("Enter your choice (1/2/3/4/5/6/7): ").strip()
                if algorithm_choice not in {"1", "2", "3", "4", "5", "6", "7"}:
                    raise ValueError("Invalid choice. Please choose a number between 1 and 7.")
                break
            except ValueError as e:
                print(e)

    output_file = "optimal_timetable_output.txt"
    algorithm_used = "Unknown Algorithm" 
    best_schedule = []
    best_fitness = 0
    elapsed_time = None

    if algorithm_choice == '2':  
        logger.info("\n--- Starting All Algorithms for Comparison ---\n")       
        with open("logs/final_output.log", "w") as log_file:
            log_file.write("All Algorithms - Final Comparison Results\n")

        comparison_start_time = time.time()
    
        algorithms = [
            ("Genetic Algorithm", genetic_algorithm),
            ("A* Algorithm", a_star_algorithm),
            ("Simulated Annealing", simulated_annealing),
            ("Hill Climbing", hill_climbing),
            ("Tabu Search", tabu_search),
        ]

        all_schedules = []

        for algo_name, algo_func in algorithms:
            logger.info(f"\n--- Starting {algo_name} ---\n")
            best_schedule, best_fitness, elapsed_time, csv_path = algo_func(logger)
            all_schedules.append((algo_name, best_schedule, best_fitness, elapsed_time))

            # Log each algorithm's final result in a consistent format
            with open("logs/final_output.log", "a") as log_file:
                log_file.write(f"\n{algo_name} - Final Results\n")
                log_file.write(f"Best Fitness: {best_fitness}\n")
                log_file.write(f"Time Taken: {elapsed_time:.2f} seconds\n")
                log_file.write("Best Timetable Configuration:\n")
                for entry in best_schedule:
                    log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}\n")

            # Plot progress for each algorithm if applicable
            if csv_path:
                plot_progress(csv_path, algo_name)

        # Generate comparison bar graph
        plot_comparison_bar_graph(all_schedules)

        logger.info("\n--- All Algorithms for Comparison Ended ---\n")

        # Determine the best algorithm based on fitness score
        best_algorithm, best_schedule, best_fitness, best_time = max(all_schedules, key=lambda x: (x[2], -x[3]))

        # Log the best algorithm
        with open("logs/final_output.log", "a") as log_file:
            log_file.write("\n--- Best Algorithm ---\n")
            log_file.write(f"Best Algorithm: {best_algorithm}\n")
            log_file.write(f"Best Fitness: {best_fitness}\n")
            log_file.write(f"Time Taken: {best_time:.2f} seconds\n")
            log_file.write("Best Timetable Configuration:\n")
            for entry in best_schedule:
                log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}\n")

    elif algorithm_choice == '1':  
        logger.info("\n--- Starting CSP ---\n")
        best_schedule, schedule_size, elapsed_time, csv_path = solve_scheduling(logger)
        algorithm_used = "CSP"

        with open("logs/final_output.log", "a") as log_file:
            log_file.write("\nResults from CSP:\n")
            log_file.write("Best Timetable Configuration:\n")
            for entry in best_schedule:
                log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}\n")
            log_file.write(f"\nNumber of Entries: {schedule_size}\n")  # Log number of entries
            log_file.write(f"Time taken: {elapsed_time:.2f} seconds\n")

        logger.info(f"--- CSP Ended ---\nTime Taken: {elapsed_time:.2f} seconds")

    else: 
        algo_functions = {
            '3': ("Genetic Algorithm", genetic_algorithm),
            '4': ("A* Algorithm", a_star_algorithm),
            '5': ("Simulated Annealing", simulated_annealing),
            '6': ("Hill Climbing", hill_climbing),
            '7': ("Tabu Search", tabu_search),
        }
        if algorithm_choice in algo_functions:
            algo_name, algo_func = algo_functions[algorithm_choice]
            logger.info(f"\n--- Starting {algo_name} ---\n")
            best_schedule, best_fitness, elapsed_time, csv_path = algo_func(logger)

            # Log the individual algorithm's results in final_output.log
            with open("logs/final_output.log", "a") as log_file:
                log_file.write(f"\n{algo_name} - Final Results\n")
                log_file.write(f"Best Fitness: {best_fitness}\n")
                log_file.write(f"Time Taken: {elapsed_time:.2f} seconds\n")
                log_file.write("Best Timetable Configuration:\n")
                for entry in best_schedule:
                    log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}\n")

            if csv_path:
                plot_progress(csv_path, algo_name)

            algorithm_used = algo_name
            logger.info(f"\n--- {algo_name} Ended ---\n")

    # Write results to the output file for the selected algorithm
    with open(output_file, "w") as file:
        file.write(f"Results from {algorithm_used}:\n")
        file.write("Best Timetable Configuration:\n")
        for entry in best_schedule:
            file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}, Day: {entry['day']}\n")
        file.write(f"\nFitness Score: {best_fitness}\n")
        if elapsed_time:
            file.write(f"Time taken: {elapsed_time:.2f} seconds\n")

    return csv_path, algorithm_used


if __name__ == "__main__":
    main()
