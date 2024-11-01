from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# Define paths
log_dir = 'logs'
output_file = 'output/final_output.txt'


def get_latest_log():
    """Read the latest log file contents."""
    try:
        # Check if the log directory exists and contains log files
        if not os.path.exists(log_dir) or not os.listdir(log_dir):
            return "No log files available."

        log_files = sorted(
            [f for f in os.listdir(log_dir) if f.startswith("timetable_optimization_")],
            key=lambda x: os.path.getmtime(os.path.join(log_dir, x))
        )
        if log_files:
            latest_log_file = os.path.join(log_dir, log_files[-1])
            with open(latest_log_file, 'r') as file:
                logs = file.read()
            return logs
        else:
            return "No log files available."
    except Exception as e:
        return f"Error reading log files: {e}"


@app.route('/')
def index():
    # Read the final output file for timetable
    try:
        with open(output_file, 'r') as file:
            timetable = [line.strip().split(', ') for line in file.readlines()]
            timetable = [
                {"course": entry[0].split(": ")[1], "room": entry[1].split(": ")[1], 
                 "timeslot": entry[2].split(": ")[1], "teacher": entry[3].split(": ")[1]}
                for entry in timetable if len(entry) == 4
            ]
    except FileNotFoundError:
        timetable = []

    # Extract unique courses and teachers for display
    unique_courses = list(set(entry['course'] for entry in timetable))
    unique_teachers = list(set(entry['teacher'] for entry in timetable))

    return render_template('index.html', timetable=timetable, unique_courses=unique_courses, unique_teachers=unique_teachers)


@app.route('/logs')
def fetch_logs():
    # Fetch logs when requested
    logs = get_latest_log()
    return jsonify(logs=logs)


@app.route('/filter_timetable')
def filter_timetable():
    # Get filter parameters from request
    course_query = request.args.get('course', '').lower()
    teacher_query = request.args.get('teacher', '').lower()

    # Read the final output file
    try:
        with open(output_file, 'r') as file:
            timetable = [line.strip().split(', ') for line in file.readlines()]
            timetable = [
                {"course": entry[0].split(": ")[1], "room": entry[1].split(": ")[1], 
                 "timeslot": entry[2].split(": ")[1], "teacher": entry[3].split(": ")[1]}
                for entry in timetable if len(entry) == 4
            ]
    except FileNotFoundError:
        timetable = []

    # Filter the timetable based on search queries
    filtered_timetable = [
        entry for entry in timetable
        if (course_query in entry['course'].lower() if course_query else True) and
           (teacher_query in entry['teacher'].lower() if teacher_query else True)
    ]

    # Check if no results found and print a message to console
    if not filtered_timetable:
        print("No results found for the given course and/or teacher.")

    return jsonify(timetable=filtered_timetable)


if __name__ == "__main__":
    app.run(debug=True)
