# Timetable Optimization Project

This project provides an optimized timetable generator using multiple search algorithms, including Genetic Algorithm, Real-Time A* (RTA*), Simulated Annealing, Hill Climbing, and Tabu Search. Each algorithm applies constraints such as room capacity, teacher availability, and teacher-course assignment limits to generate the most suitable timetable based on a fitness score.

## Features

- **Multiple Optimization Algorithms**: Choose between Genetic Algorithm, RTA\*, Simulated Annealing, Hill Climbing, and Tabu Search.
- **Constraint Handling**:
  - Room capacity enforcement.
  - Teacher availability.
  - Unique teacher-course assignments.
  - Consecutive class penalties.
  - Timeslot conflict avoidance.
- **Fitness Evaluation**: Generates a fitness score based on constraint satisfaction and optimization objectives.
- **Logging**: Logs detailed information on each algorithm’s performance and comparison results.

## Project Structure

```
Heuristic_Search_Project/
├── data/
│   ├── input_data.py           # Contains course, teacher, room, and timeslot data
├── logs/
│   ├── detailed_logs.log       # Logs details of each iteration for all algorithms
│   ├── final_output.log        # Logs final comparison results and best timetable
├── src/
│   ├── main.py                 # Entry point for running algorithms
│   ├── fitness.py              # Fitness function for timetable evaluation
│   ├── genetic_algorithm.py    # Genetic Algorithm implementation
│   ├── rta_star.py             # RTA* Algorithm implementation
│   ├── simulated_annealing.py  # Simulated Annealing implementation
│   ├── hill_climbing.py        # Hill Climbing implementation
│   ├── tabu_search.py          # Tabu Search implementation
│   ├── app.py                  # Flask application for web UI
├── templates/
│   ├── welcome.html            # Welcome page for selecting algorithm
│   ├── results.html            # Displays results for selected algorithm
│   ├── comparison.html         # Comparison view for all algorithms
│   ├── detailed_logs.html      # Detailed logs view
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/Heuristic_Search_Project.git
   cd Heuristic_Search_Project
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage

### 1. Command-Line Interface

Run the main Python script to choose an algorithm and generate a timetable:

```bash
python3 -m src.main
```

### 2. Web Interface

You can also run the project as a Flask web application:

```bash
python3 -m src.app
```

Navigate to `http://127.0.0.1:5000` in your browser to access the application.

## Configuration

- **`data/input_data.py`**: Modify this file to add or update courses, teachers, rooms, and timeslots.
- **Logging**: Logs are stored in the `logs` folder:
  - `detailed_logs.log` records each iteration’s details.
  - `final_output.log` records final results and comparison data.

## Algorithm Descriptions

Each algorithm aims to optimize the timetable based on defined constraints. Here’s a summary:

- **Genetic Algorithm**: Evolves a population of timetables through selection, crossover, and mutation.
- **RTA\***: Uses a real-time search to evaluate timetables in constrained steps.
- **Simulated Annealing**: Searches for an optimal solution by exploring neighbors with a decreasing probability of accepting worse solutions.
- **Hill Climbing**: Starts with an initial solution and iteratively moves to a better neighboring solution.
- **Tabu Search**: Explores the solution space while avoiding cycles through the use of a tabu list.

## Fitness Calculation

The fitness function is defined in `fitness.py` and calculates a score based on these criteria:

- Room capacity checks (penalty if exceeded)
- Teacher availability (penalty if violated)
- Unique timeslot assignments
- Teacher-course matching
- Constraints on maximum daily courses per teacher
- Penalties for consecutive classes and timeslot conflicts

## Example Workflow

1. Run the application.
2. Select an algorithm or choose "Optimal of All" for a comprehensive comparison.
3. View the timetable results, logs, and algorithm comparisons through the web interface or log files.

## Additional Notes

- **Dependencies**: Ensure Flask is installed for the web interface.
- **Logging**: Logs reset on each run. To keep previous logs, back them up before each run.

Enjoy using the Timetable Optimization Project! Feel free to contribute or suggest improvements.

```

```
