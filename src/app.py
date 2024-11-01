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
    try:
        with open(output_file, 'r') as file:
            timetable = [
                line.strip().split(', ') for line in file.readlines()
            ]
            timetable = [
                {"course": entry[0].split(": ")[1], "room": entry[1].split(": ")[1],
                 "timeslot": entry[2].split(": ")[1], "teacher": entry[3].split(": ")[1]}
                for entry in timetable if len(entry) == 4
            ]
    except FileNotFoundError:
        timetable = []

    unique_courses = list(set(entry['course'] for entry in timetable))
    unique_teachers = list(set(entry['teacher'] for entry in timetable))

    return render_template('index.html', timetable=timetable, unique_courses=unique_courses, unique_teachers=unique_teachers)

@app.route('/logs')
def fetch_logs():
    logs = get_latest_log()
    return jsonify(logs=logs)

@app.route('/filter_timetable')
def filter_timetable():
    course = request.args.get("course", "")
    teacher = request.args.get("teacher", "")

    try:
        with open(output_file, 'r') as file:
            timetable = [
                line.strip().split(', ') for line in file.readlines()
            ]
            timetable = [
                {"course": entry[0].split(": ")[1], "room": entry[1].split(": ")[1],
                 "timeslot": entry[2].split(": ")[1], "teacher": entry[3].split(": ")[1]}
                for entry in timetable if len(entry) == 4
            ]
    except FileNotFoundError:
        timetable = []

    if course:
        timetable = [entry for entry in timetable if entry['course'] == course]
    if teacher:
        timetable = [entry for entry in timetable if entry['teacher'] == teacher]

    return jsonify(timetable=timetable)

if __name__ == "__main__":
    app.run(debug=True)
