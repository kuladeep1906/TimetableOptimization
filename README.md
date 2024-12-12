# **Timetable Optimization Using Heuristic Search and Constraint Processing**

## **Overview**
This project is a sophisticated timetable optimization system that uses advanced algorithms to generate efficient and conflict-free schedules. It is designed to handle complex constraints such as teacher availability, room capacity, course prerequisites, and preferred timeslots. The system provides a user-friendly web interface for selecting optimization algorithms and visualizing results, including progress graphs and algorithm comparisons.

---

## **Features**
- **Multiple Optimization Algorithms:**
  - Constraint Satisfaction Problem (CSP)
  - Genetic Algorithm
  - A* Algorithm
  - Simulated Annealing
  - Hill Climbing
  - Tabu Search
- **Interactive Web Interface:**
  - Select algorithms.
  - View optimized timetables.
  - Compare algorithm performances with progress and comparison graphs.
- **Comprehensive Constraints:**
  - Room capacities and teacher availability.
  - Preferred timeslots, rooms, and balanced utilization.
  - Avoidance of consecutive classes for teachers.
- **Visualization:**
  - Progress graphs for algorithm iterations.
  - Bar graphs comparing fitness scores and execution times across algorithms.
- **Detailed Logs:**
  - View algorithm-specific logs and outputs for debugging and analysis.

---

## **Project Structure**
```
TimetableOptimization/
├── data/
│   ├── input_data.py           # Defines courses, teachers, rooms, days, and timeslots.
├── src/
│   ├── genetic_algorithm.py    # Genetic Algorithm implementation.
│   ├── a_star.py               # A* Algorithm implementation.
│   ├── simulated_annealing.py  # Simulated Annealing implementation.
│   ├── hill_climbing.py        # Hill Climbing implementation.
│   ├── tabu_search.py          # Tabu Search implementation.
│   ├── csp.py                  # CSP implementation.
│   ├── fitness.py              # Fitness evaluation for timetables.
│   ├── main.py                 # Orchestrates algorithm execution and comparison.
|   ├── app.py                  # Flask application to serve the web interface.
├── templates/
│   ├── welcome.html            # Homepage for algorithm selection.
│   ├── results.html            # Displays optimized timetables.
│   ├── comparison.html         # Shows progress and comparison graphs.
│   ├── logs.html               # Displays detailed logs.
│   ├── detailed_logs.html      # Detailed breakdown of algorithm outputs.  
├── static/
│   ├── progress/               # Contains generated progress and comparison graphs.                    
├── README.md                   # Project documentation.
├── requirements.txt            # Python dependencies.
```

---

## **Installation**

### **Prerequisites**
- Python 3.9+
- pip (Python package manager)

### **Steps**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/TimetableOptimization.git
   cd TimetableOptimization
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python3 -m src.app
   ```

4. **Open the web interface:**
   Visit `http://127.0.0.1:5000` in your browser.

---

## **Usage**
1. **Home Page:**
   - Select an algorithm from the dropdown menu.
   - Click "View Results" to generate an optimized timetable.

2. **Results Page:**
   - View the optimized timetable displayed in a grid format.
   - Access options to compare algorithms or analyze detailed logs.

3. **Comparison Page:**
   - View progress graphs for all algorithms.
   - Analyze a bar graph comparing fitness scores and execution times.

4. **Logs Page:**
   - Access detailed algorithm-specific logs for debugging and analysis.

---

## **Algorithms**
Each algorithm is designed to optimize the timetable by balancing constraints and achieving the highest fitness score.

1. **Constraint Satisfaction Problem (CSP):**
   - Uses backtracking to satisfy all constraints.
2. **Genetic Algorithm:**
   - Mimics evolutionary processes (selection, crossover, mutation).
3. **A* Algorithm:**
   - Explores states using heuristic-driven search.
4. **Simulated Annealing:**
   - Escapes local optima using probabilistic decisions.
5. **Hill Climbing:**
   - Iteratively improves solutions with restarts to avoid local optima.
6. **Tabu Search:**
   - Uses a memory-based mechanism to avoid revisiting solutions.

---

## **Constraints**
1. **Hard Constraints** (must be satisfied):
   - Room capacity must not be exceeded.
   - Teachers must be available for their assigned timeslots.
   - Teachers must only teach assigned courses.
   - Avoid overlapping timeslots for rooms or teachers.

2. **Soft Constraints** (improved for better schedules):
   - Assign preferred rooms for courses.
   - Use teacher-preferred timeslots and days.
   - Balance room and day utilization.
   - Avoid consecutive classes for teachers.

---

## **Visualization**
- **Progress Graphs:** Track fitness scores across iterations for each algorithm.
- **Comparison Graphs:** Compare fitness scores and execution times across all algorithms.

---

## **Technologies Used**
- **Programming Language:** Python
- **Framework:** Flask
- **Visualization:** Matplotlib, HTML/CSS
- **Frontend:** HTML, CSS, JavaScript
- **Data Management:** pandas, NumPy

---

## **Future Enhancements**
- Enable scheduling for multiple campuses or departments.
- Provide a downloadable timetable as a PDF or Excel file.


