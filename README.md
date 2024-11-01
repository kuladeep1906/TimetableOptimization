```markdown
# Timetable Generator

This project is an optimized timetable generator built using various heuristic and AI-based algorithms. It generates a feasible timetable by taking into account constraints like teacher availability, room capacity, and preferred timeslots for courses. The project also includes a web-based user interface to visualize the optimized timetable and access detailed logs.

## Features

- **Multiple Optimization Algorithms**: Uses Genetic Algorithm, Simulated Annealing, Real-Time A* (RTA*), and Tabu Search to optimize timetables.
- **Customizable Constraints**: Configurable fitness functions to account for room capacity, teacher availability, preferred rooms, and course load.
- **Web Interface**: Visualize the timetable and access detailed optimization logs.
- **Log Management**: Generates log files for each run, retaining only the latest logs to save storage.

## How It Works

1. **Generate Initial Population**: Using constraint programming, an initial population of timetables is created to satisfy the hard constraints.
2. **Genetic Algorithm**: Optimizes the initial population to improve the timetable based on the fitness score.
3. **Simulated Annealing**: Further refines the solution by exploring other feasible solutions and reducing penalties.
4. **Real-Time A\***: Addresses specific constraint violations by generating alternative solutions for problematic entries.
5. **Tabu Search**: Final optimization stage to further improve the timetable and avoid previous solutions.

## Project Structure

The project is structured as follows:
```

timetable-generator/
│
├── src/ # Source code files
│ ├── main.py # Main script to run the timetable generator
│ ├── genetic*algorithm.py # Genetic Algorithm implementation
│ ├── rta_star.py # Real-Time A\* Algorithm implementation
│ ├── fitness.py # Fitness function and constraints
│ ├── simulated_annealing.py # Simulated Annealing implementation
│ ├── tabu_search.py # Tabu Search optimization
│ ├── constraint_programming.py# Initial feasible timetable generation
│ ├── timetable.py # Timetable class definition
│ └── app.py # Flask application for UI
│
├── data/ # Input data for courses, rooms, teachers
│ └── input_data.py # Teacher, course, and timeslot data
│
├── templates/ # HTML templates for the web interface
│ └── index.html # Main UI template
│
├── static/ # Static files like CSS and JS for the web interface
│ └── styles.css # CSS file for styling the UI
│
├── logs/ # Logs directory for optimization process logs
│ └── timetable_optimization*<timestamp>.txt # Log files with details of each run
│
├── output/ # Directory for final output files
│ └── final_output.txt # Final optimized timetable
│
├── requirements.txt # Project dependencies
└── README.md # Project documentation (this file)

````

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Heuristic_search_project.git
   cd timetable-generator
````

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

1. **Run the main script**:
   This will generate the optimized timetable and save the output in `output/final_output.txt`.

   ```bash
   python3 -m src/main.py
   ```

2. **Launch the web interface**:
   The Flask web application displays the final timetable and allows users to view logs.

   ```bash
   python3 -m src/app.py
   ```

3. **Access the interface**:
   Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to view the timetable.

## Configuration

- **Data**: Modify `data/input_data.py` to adjust the courses, teachers, rooms, and timeslots.
- **Constraints**: Adjust constraints in `src/fitness.py` as needed to prioritize different scheduling rules.
- **Log Retention**: Set the number of logs to retain in `src/main.py` in the `clean_old_logs` function.

## License

This project is licensed under the MIT License.
