```markdown
# Timetable Scheduling Using Heuristic Algorithms

## Overview
This project implements a **timetable scheduling system** using various heuristic algorithms and **Constraint Satisfaction Problem (CSP)** techniques. It aims to generate optimal timetables for courses, teachers, rooms, and timeslots while adhering to constraints like room capacity, teacher preferences, avoiding consecutive classes, and balancing utilization of resources.

### Algorithms Implemented:
1. **Genetic Algorithm**
2. **Real-Time A*** (RTA*)
3. **Simulated Annealing**
4. **Hill Climbing**
5. **Tabu Search**
6. **Constraint Satisfaction Problem (CSP)**

The system considers penalties for constraint violations and rewards for satisfying preferences, such as teacher-preferred days or times.

---

## Features
- **Flexible Constraints**: Ensures valid timetables by avoiding room conflicts, teacher conflicts, and consecutive classes.
- **Balanced Utilization**: Distributes courses evenly across days and rooms to avoid overcrowding or underutilization.
- **Multiple Heuristic Algorithms**: Supports comparative analysis of results across various algorithms.
- **Logging**: Tracks the scheduling process, including constraint violations, improvements, and final results.
- **CSV Output**: Logs progress for each algorithm into CSV files for visualization and debugging.

---

## Project Structure

```plaintext
project/
├── data/
│   ├── input_data.py         # Contains input datasets (Courses, Teachers, Rooms, Timeslots)
├── src/
│   ├── genetic_algorithm.py  # Implementation of Genetic Algorithm
│   ├── rta_star.py           # Implementation of Real-Time A*
│   ├── simulated_annealing.py # Implementation of Simulated Annealing
│   ├── hill_climbing.py      # Implementation of Hill Climbing
│   ├── tabu_search.py        # Implementation of Tabu Search
│   ├── csp.py                # CSP-based scheduling algorithm
│   ├── fitness.py            # Fitness evaluation logic
│   ├── utils.py              # Utility functions
├── progress/                 # Folder to store progress logs (CSV files)
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
```

---

## Getting Started

### Prerequisites
- Python 3.9 or higher
- A virtual environment (recommended for managing dependencies)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/timetable-scheduling.git
   cd timetable-scheduling
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Run a Specific Algorithm
1. **Run Genetic Algorithm**:
   ```bash
   python src/genetic_algorithm.py
   ```

2. **Run Real-Time A***:
   ```bash
   python src/rta_star.py
   ```

3. **Run CSP Algorithm**:
   ```bash
   python src/csp.py
   ```

### Customize Input Data
Modify `data/input_data.py` to update:
- **Courses**: Names, students, preferred rooms, teacher assignments, and instances per week.
- **Teachers**: Availability, preferred days, and timeslots.
- **Rooms**: Capacity and names.
- **Timeslots**: Available times.

---

## Outputs

1. **Logs**:
   Each algorithm logs its progress in the `progress/` folder as a CSV file.

2. **Final Results**:
   The best timetable configuration is logged, including:
   - Course
   - Room
   - Teacher
   - Day
   - Timeslot

3. **Visualization**:
   Use the logged CSV files to visualize results and compare performance.

---

## Constraints Considered
1. **Room Capacity**: Ensures rooms can accommodate all students.
2. **Teacher Availability**: Schedules teachers only during their available times.
3. **Consecutive Classes**: Avoids consecutive classes for teachers.
4. **Preferred Days/Timeslots**: Rewards schedules that align with teacher preferences.
5. **Room and Day Balancing**: Evenly distributes courses across all rooms and days.

---

## Example Input (data/input_data.py)

```python
COURSES = [
    {'name': 'Data Science', 'students': 30, 'preferred_rooms': ['Room 1', 'Room 2'], 'teacher': 'Ms. D', 'instances_per_week': 2},
    {'name': 'AI', 'students': 35, 'preferred_rooms': ['Room 3'], 'teacher': 'Mr. A', 'instances_per_week': 3},
    # Add more courses
]

TEACHERS = [
    {'name': 'Ms. D', 'availability': ['9 AM', '10 AM', '11 AM'], 'preferred_days': ['Monday', 'Wednesday', 'Friday']},
    {'name': 'Mr. A', 'availability': ['10 AM', '12 PM', '2 PM'], 'preferred_days': ['Tuesday', 'Thursday']},
    # Add more teachers
]

ROOMS = [
    {'name': 'Room 1', 'capacity': 40},
    {'name': 'Room 2', 'capacity': 30},
    # Add more rooms
]

TIMESLOTS = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM']
```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributions
Contributions are welcome! Feel free to fork this repository, create a branch, and submit a pull request.

For questions or issues, open an issue on GitHub or contact [your-email@example.com](mailto:your-email@example.com).
```

---

