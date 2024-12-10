from flask import Flask, render_template, request, redirect, url_for
from src.main import main as run_main_algorithm
from src.main import plot_progress, plot_comparison_bar_graph  
import os
import matplotlib
matplotlib.use('Agg') 

app = Flask(__name__, static_folder="../static")


# Ensure necessary directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("progress", exist_ok=True)

def clear_log_files():
    """Clear the contents of the log files or create them if they don't exist."""
    log_files = ["logs/detailed_logs.log", "logs/final_output.log"]
    for log_file in log_files:
        with open(log_file, "w") as file:
            file.write("") 

@app.route("/")
def home():
    return redirect(url_for("welcome"))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        selected_algorithm = request.form.get("algorithm_choice")
        if selected_algorithm and selected_algorithm != "choose":
            # Clear log files whenever a new selection is made
            clear_log_files()
            return redirect(url_for("results", algorithm=selected_algorithm))
    return render_template("welcome.html", algorithm_choice="choose")

@app.route("/results")
def results():
    algorithm_choice = request.args.get("algorithm")
    filtered_results = []
    timeslots = []
    days = []
    graph_path = None

    if algorithm_choice and algorithm_choice != "choose":
        # Run the selected algorithm
        csv_path, algo_name = run_main_algorithm(algorithm_choice)
        results = read_output_file()

        # Filter out fitness score and time from results
        filtered_results = [entry for entry in results if "Course" in entry]

        # Define timeslots and days for rendering the timetable
        timeslots = [
            "9:00 AM - 10:00 AM",
            "10:00 AM - 11:00 AM",
            "11:00 AM - 12:00 PM",
            "12:00 PM - 1:00 PM",
            "1:00 PM - 2:00 PM",
            "2:00 PM - 3:00 PM",
            "3:00 PM - 4:00 PM",
            "4:00 PM - 5:00 PM",
            "5:00 PM - 6:00 PM",
            "6:00 PM - 7:00 PM",
        ]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Check and generate progress graph if available
        if csv_path:
            plot_progress(csv_path, algo_name)
            graph_path = f"static/{csv_path}"

       
        print("Filtered Results:", filtered_results)
        print("Timeslots:", timeslots)
        print("Days:", days)
    else:
        print("No valid algorithm choice or results to display.")

    return render_template(
        "results.html",
        results=filtered_results,
        timeslots=timeslots,
        days=days,
        graph_path=graph_path,
        algorithm_choice=algorithm_choice,
    )

@app.route("/comparison")
def show_comparison():
    algorithm_choice = request.args.get("algorithm_choice", "none")
    print(f"Algorithm choice received in comparison: {algorithm_choice}")  

    if algorithm_choice == "2":
        print("Displaying comparison for all algorithms.")  

       
        graph_paths = {
            "Genetic Algorithm": "/static/progress/genetic_algorithm_progress.png",
            "A*": "/static/progress/astar_algorithm_progress.png",
            "Simulated Annealing": "/static/progress/simulated_annealing_progress.png",
            "Hill Climbing": "/static/progress/hill_climbing_progress.png",
            "Tabu Search": "/static/progress/tabu_search_progress.png",
        }
    else:
        print("Displaying message for a single algorithm.")  
        graph_paths = None  # No graphs for a single algorithm

    with open("logs/final_output.log", "r") as file:
        comparison_log = file.read()

    return render_template(
        "comparison.html", 
        title="Comparison Log", 
        log_content=comparison_log, 
        algorithm_choice=algorithm_choice,
        graph_paths=graph_paths,
    )

@app.route("/logs")
def show_logs():
    with open("logs/detailed_logs.log", "r") as file:
        detailed_log = file.read()
    return render_template("detailed_logs.html", title="Detailed Logs", log_content=detailed_log)

def read_output_file(csp=False):
    results = []
    with open("optimal_timetable_output.txt", "r") as file:
        current_algorithm = file.readline().strip()  
        file.readline() 
        for line in file:
            if line.startswith("Course:"):
                parts = line.strip().split(", ")
                course_data = {part.split(": ")[0]: part.split(": ")[1] for part in parts}
                results.append(course_data)
    return results


if __name__ == "__main__":
    app.run(debug=True)
