# Timetable Optimization System

This project is a comprehensive timetable optimization system that employs various algorithms to generate optimal timetables based on specified constraints. The system is designed to be flexible, user-friendly, and visually informative, providing progress graphs, comparison features, and detailed logging.

## Features

### 1. Algorithm Support

The system supports multiple algorithms for timetable generation:

- **Genetic Algorithm**
- **RTA\* Algorithm**
- **Simulated Annealing**
- **Hill Climbing**
- **Tabu Search**

### 2. Comparison of Algorithms

- Generates a comparison of fitness scores and execution times for all algorithms.
- Displays line graphs showing the progress of fitness scores for each algorithm.
- Displays a bar graph comparing the final fitness scores and execution times of all algorithms.
- Logs detailed information about the best timetable configuration for each algorithm.

### 3. Progress Graphs

- Line graphs are generated for each algorithm showing the progress of fitness scores across generations or iterations.
- Bar graphs compare the fitness scores and execution times of all algorithms.

### 4. User Interface Features

- Interactive UI with options to select algorithms and view results.
- **Loading Indicator**: A loading spinner is displayed while generating the timetable.
- **Search Functionality**: Search for specific courses or teachers in the generated timetable.
- **Number of Entries Display**: Shows the total number of entries in the timetable.

### 5. Logging and Analysis

- Detailed logs for each algorithm run.
- Final comparison results for all algorithms, including the best timetable configuration, fitness scores, and execution times.

### 6. Responsive Design

The UI is designed to be user-friendly and responsive, with dynamic updates and animations for better user experience.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/timetable-optimization.git
   cd timetable-optimization
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:

   ```bash
   python src/app.py
   ```

4. Open the application in your browser at:
   ```
   http://127.0.0.1:5000
   ```

---

## Project Structure

- **src/**: Contains the core application logic.
  - `genetic_algorithm.py`: Genetic algorithm implementation.
  - `hill_climbing.py`: Hill climbing algorithm implementation.
  - `rta_star.py`: RTA\* algorithm implementation.
  - `simulated_annealing.py`: Simulated annealing implementation.
  - `tabu_search.py`: Tabu search implementation.
  - `fitness.py`: Fitness calculation logic.
  - `app.py`: Flask application logic.
  - `main.py`: Entry point for running algorithms.
- **data/**: Contains input data for courses, teachers, rooms, and timeslots.
- **static/**: Static files for progress graphs.
- **templates/**: HTML templates for the Flask application.
- **logs/**: Contains detailed logs and final output logs.
- **progress/**: Stores progress CSV files for each algorithm.

---

## How to Use

1. Start the application by running:

   ```bash
   python src/app.py
   ```

2. Navigate to the **Welcome Page** and select an algorithm from the dropdown menu.

3. **Loading Spinner**: A loading spinner will appear while the timetable is being generated.

4. View the generated timetable with the following features:

   - **Search Functionality**: Filter results by course or teacher name.
   - **Number of Entries**: Displays the total number of entries in the timetable.

5. Navigate to the **Comparison Page** to:
   - View line graphs for the progress of all algorithms.
   - View a bar graph comparing fitness scores and execution times.
   - Read detailed logs of the comparison process.

---

## Visualization

### Progress Graphs

- **Line Graphs**: Display the progression of fitness scores for each algorithm.
- **Bar Graph**: Compare fitness scores and execution times across all algorithms.

### Example Graphs:

- Genetic Algorithm Progress
- RTA\* Algorithm Progress
- Simulated Annealing Progress
- Hill Climbing Progress
- Tabu Search Progress

---

## Logs

- **Detailed Logs**: Available in the `logs/detailed_logs.log` file.
- **Final Output Logs**: Available in the `logs/final_output.log` file.

---

## Future Enhancements

- Enhance UI responsiveness and interactivity.
- Add dynamic constraints customization.

---

## License

This project is licensed under the MIT License.

```

### Highlights
- Added **loading indicator**, **bar graph comparison**, and **number of entries display** in the features section.
- Updated project structure to include new files and directories.
- Explained the process of using the new features in the **How to Use** section.

You can further customize this to align with your specific repository name and URL.
```
