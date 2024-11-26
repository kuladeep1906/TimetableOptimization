import logging
import os
import time
import matplotlib.pyplot as plt  # For plotting graphs
from .genetic_algorithm import genetic_algorithm
from .rta_star import rta_star_algorithm
from .simulated_annealing import simulated_annealing
from .hill_climbing import hill_climbing
from .tabu_search import tabu_search
import pandas as pd  # For handling CSV files
import numpy as np  # For handling data in graphs

# Ensure the logs folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Ensure the progress CSV folder exists
if not os.path.exists("progress"):
    os.makedirs("progress")

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
            color='green',  # Green for Current Best Fitness
            linestyle='--', 
            marker='x'
        )
        
        plt.xlabel("Generation", fontsize=14)
        plt.ylabel("Fitness", fontsize=14)
        plt.title(f"Algorithm Progress for {algorithm_name}", fontsize=16, fontweight='bold')
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Use constrained layout to avoid tight layout issues
        plt.gcf().subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9)

        # Construct output path
        sanitized_name = algorithm_name.replace(' ', '_').replace('*', 'star').lower()
        output_path = os.path.join(progress_dir, f"{sanitized_name}_progress.png")
        
        # Save the plot
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

        x = np.arange(len(algo_names))  # X-axis positions

        # Create bar graph
        fig, ax1 = plt.subplots(figsize=(14, 8))
        bar_width = 0.35

        # Bar for fitness scores
        ax1.bar(x - bar_width/2, fitness_scores, bar_width, label="Fitness Score", color='blue', alpha=0.7)

        # Secondary Y-axis for execution times
        ax2 = ax1.twinx()
        ax2.bar(x + bar_width/2, execution_times, bar_width, label="Execution Time (s)", color='orange', alpha=0.7)

        ax1.set_xlabel("Algorithms", fontsize=14)
        ax1.set_ylabel("Fitness Score", fontsize=14, color='blue')
        ax2.set_ylabel("Execution Time (s)", fontsize=14, color='orange')
        ax1.set_title("Comparison of Fitness Scores and Execution Times", fontsize=16, fontweight='bold')

        # Add labels and legend
        ax1.set_xticks(x)
        ax1.set_xticklabels(algo_names, fontsize=12)
        ax1.tick_params(axis='y', labelcolor='blue')
        ax2.tick_params(axis='y', labelcolor='orange')

        fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9), fontsize=12)
        fig.tight_layout()

        # Save the graph
        output_path = os.path.join(progress_dir, "comparison_bar_graph.png")
        plt.savefig(output_path)
        plt.close()

        print(f"Comparison bar graph saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred while creating the comparison bar graph: {e}")

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

    if algorithm_choice == '6':
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
            best_schedule, best_fitness, elapsed_time, csv_path = algo_func(logger)
            all_schedules.append((algo_name, best_schedule, best_fitness, elapsed_time))

            # Log each algorithm's final result in a consistent format
            with open("logs/final_output.log", "a") as log_file:
                log_file.write(f"\n{algo_name} - Final Results\n")
                log_file.write(f"Best Fitness: {best_fitness}\n")
                log_file.write(f"Time Taken: {elapsed_time:.2f} seconds\n")
                log_file.write("Best Timetable Configuration:\n")
                for entry in best_schedule:
                    log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}\n")

            # Plot progress for each algorithm
            plot_progress(csv_path, algo_name)

        # Generate comparison bar graph
        plot_comparison_bar_graph(all_schedules)

        logger.info("\n--- All Algorithms for Comparison Ended ---\n")

        # Calculate total elapsed time for running all algorithms
        comparison_end_time = time.time()
        total_comparison_time = comparison_end_time - comparison_start_time

        # Determine the best algorithm based on fitness score (higher is better)
        best_algorithm, best_schedule, best_fitness, best_time = max(all_schedules, key=lambda x: (x[2], -x[3]))

        # Log the best algorithm
        with open("logs/final_output.log", "a") as log_file:
            log_file.write("\n--- Best Algorithm ---\n")
            log_file.write(f"Best Algorithm: {best_algorithm}\n")
            log_file.write(f"Best Fitness: {best_fitness}\n")
            log_file.write(f"Time Taken: {best_time:.2f} seconds\n")
            log_file.write("Best Timetable Configuration:\n")
            for entry in best_schedule:
                log_file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}\n")

        print("\n--- Best Algorithm ---")
        print(f"Best Algorithm: {best_algorithm}")
        print(f"Best Fitness: {best_fitness}")
        print(f"Time Taken: {best_time:.2f} seconds")
        print("Best Timetable Configuration:")
        for entry in best_schedule:
            print(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}")

        # Log total time taken for comparison
        with open("logs/final_output.log", "a") as log_file:
            log_file.write("\n--- Total Comparison Time ---\n")
            log_file.write(f"Total Time Taken to Compare All Algorithms: {total_comparison_time:.2f} seconds\n")

    else:
        # Handle single algorithm choice
        algo_functions = {
            '1': ("Genetic Algorithm", genetic_algorithm),
            '2': ("RTA* Algorithm", rta_star_algorithm),
            '3': ("Simulated Annealing", simulated_annealing),
            '4': ("Hill Climbing", hill_climbing),
            '5': ("Tabu Search", tabu_search)
        }
        if algorithm_choice in algo_functions:
            algo_name, algo_func = algo_functions[algorithm_choice]
            logger.info(f"\n--- Starting {algo_name} ---\n")
            best_schedule, best_fitness, elapsed_time, csv_path = algo_func(logger)
            plot_progress(csv_path, algo_name)
            algorithm_used = algo_name
            logger.info(f"\n--- {algo_name} Ended ---\n")

    # Write results to the output file for the selected algorithm
    with open(output_file, "w") as file:
        file.write(f"Results from {algorithm_used}:\n")
        file.write("Best Timetable Configuration:\n")
        for entry in best_schedule:
            file.write(f"Course: {entry['course']}, Room: {entry['room']}, Teacher: {entry['teacher']}, Timeslot: {entry['timeslot']}\n")
        file.write(f"\nFitness Score: {best_fitness}\n")
        if elapsed_time:
            file.write(f"Time taken: {elapsed_time:.2f} seconds\n")
    return csv_path, algorithm_used


if __name__ == "__main__":
    main()
