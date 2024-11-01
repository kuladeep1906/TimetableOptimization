# Timetable Optimization Project

This project is a timetable optimization tool designed to assign courses, rooms, timeslots, and teachers to optimize scheduling based on various constraints. It leverages multiple algorithms like Genetic Algorithm, Real-Time A\*, Simulated Annealing, and Tabu Search for iterative refinement of the timetable. Additionally, a Flask-based UI displays the optimized timetable and provides filtering and log-viewing features.

## Features

- **Optimization Algorithms**:

  - **Genetic Algorithm**: Initial population-based search for optimal scheduling.
  - **Simulated Annealing**: Refines solutions by exploring the solution space while avoiding local optima.
  - **Real-Time A\***: Identifies issues and iteratively improves the timetable.
  - **Tabu Search**: Provides a final optimization by avoiding previously visited sub-optimal solutions.
  - **Constraint Programming** - Generates an initial feasible timetable that satisfies basic constraints like room capacity and teacher availability.

- **Constraints**:

  - Room capacity limits and preferred rooms for specific courses.
  - Timeslot availability and teacher preferences.
  - Avoids scheduling conflicts for rooms and teachers.

- **UI**:
  - Filter the timetable by course and teacher.
  - Option to view detailed optimization logs.

## Project Structure

The project is structured as follows:

```
timetable-generator/
│
├── src/                         # Source code files
│   ├── main.py                  # Main script to run the timetable generator
│   ├── genetic_algorithm.py     # Genetic Algorithm implementation
│   ├── rta_star.py              # Real-Time A* Algorithm implementation
│   ├── fitness.py               # Fitness function and constraints
│   ├── simulated_annealing.py   # Simulated Annealing implementation
│   ├── tabu_search.py           # Tabu Search optimization
│   ├── constraint_programming.py# Initial feasible timetable generation
│   ├── timetable.py             # Timetable class definition
│   └── app.py                   # Flask application for UI
│
├── data/                        # Input data for courses, rooms, teachers
│   └── input_data.py            # Teacher, course, and timeslot data
│
├── templates/                   # HTML templates for the web interface
│   └── index.html               # Main UI template
│   └── template.html
│
├── static/                      # Static files like CSS and JS for the web interface
│   └── style.css                # CSS file for styling the UI
│
├── logs/                        # Logs directory for optimization process logs
│   └── timetable_optimization_<timestamp>.txt # Log files with details of each run
│
├── output/                     # Directory for final output files
│   └── final_output.txt         # Final optimized timetable
│
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation (this file)
```

## Getting Started

### Prerequisites

- Python 3.9 or later
- Ensure you have `pip` installed.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/timetable-generator.git
   cd timetable-generator
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### Running the Project

1. **Run the Timetable Generator**:

   ```bash
   python3 -m src/main.py
   ```

   This will generate an optimized timetable and log the details in `logs/`.

2. **Start the Flask Web UI**:
   ```bash
   python3 -m src/app.py
   ```
   Visit `http://127.0.0.1:5000` in your browser to view the timetable, apply filters, and view optimization logs.

### Using the Filters and Log Viewer

- **Filtering**: Use the dropdown menus to filter the timetable by specific courses or teachers.
- **Show Logs**: Click the "Show Logs" button to view detailed logs of the optimization process.

## Example Data

Example courses, teachers, rooms, and timeslots are included in `data/input_data.py` for testing. You can modify these for your specific requirements.

## Customization

- **Constraints**: Modify constraints in `fitness.py` to add/remove rules or adjust penalties.
- **Algorithms**: You can adjust algorithm parameters in their respective files (e.g., `genetic_algorithm.py`, `simulated_annealing.py`).

## License

This project is open-source and available under the MIT License.
