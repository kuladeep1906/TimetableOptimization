from flask import Flask, render_template, request, redirect, url_for
from src.main import main as run_main_algorithm
import os

app = Flask(__name__)

# Ensure the logs folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

def clear_log_files():
    """Clear the contents of the log files or create them if they don't exist."""
    log_files = ["logs/detailed_logs.log", "logs/final_output.log"]
    for log_file in log_files:
        with open(log_file, "w") as file:
            file.write("")  # Clear contents by writing an empty string

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
            # Redirect to results page with the selected algorithm
            return redirect(url_for("results", algorithm=selected_algorithm))
    return render_template("welcome.html", algorithm_choice="choose")

@app.route("/results")
def results():
    algorithm_choice = request.args.get("algorithm")
    if algorithm_choice and algorithm_choice != "choose":
        # Run the algorithm and generate results
        run_main_algorithm(algorithm_choice)
        results = read_output_file()
    else:
        results = None
    return render_template("results.html", results=results, algorithm_choice=algorithm_choice)

@app.route("/comparison")
def show_comparison():
    # Try to get algorithm_choice from request arguments; if not present, assume it's "none"
    algorithm_choice = request.args.get("algorithm_choice", "none")
    print(f"Algorithm choice received in comparison: {algorithm_choice}")  # Debug print
    with open("logs/final_output.log", "r") as file:
        comparison_log = file.read()
    return render_template("comparison.html", title="Comparison Log", log_content=comparison_log, algorithm_choice=algorithm_choice)

@app.route("/logs")
def show_logs():
    with open("logs/detailed_logs.log", "r") as file:
        detailed_log = file.read()
    return render_template("detailed_logs.html", title="Detailed Logs", log_content=detailed_log)

def read_output_file():
    results = []
    with open("optimal_timetable_output.txt", "r") as file:
        current_algorithm = file.readline().strip()
        file.readline()
        for line in file:
            if line.startswith("Course:"):
                parts = line.strip().split(", ")
                course_data = {part.split(": ")[0]: part.split(": ")[1] for part in parts}
                results.append(course_data)
            elif line.startswith("Fitness Score:"):
                fitness_score = line.strip().split(": ")[1]
                results.append({"Fitness Score": fitness_score})
            elif line.startswith("Time taken:"):
                time_taken = line.strip().split(": ")[1]
                results.append({"Time taken": time_taken})
    return results

if __name__ == "__main__":
    app.run(debug=True)
