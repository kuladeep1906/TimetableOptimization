# **Timetable Generator Using Genetic Algorithm and Real-Time A\***

This project is a timetable generation system that uses a **Genetic Algorithm (GA)** and **Real-Time A\*** (RTA\*) to create an optimized schedule for courses, teachers, rooms, and timeslots. The system ensures that the schedule adheres to several constraints, including teacher-course pairings, room availability, and teacher workload balance.

## **Features**

- **Genetic Algorithm Optimization**: Produces a near-optimal timetable by evolving solutions over multiple generations.
- **Real-Time A\* Refinement**: Refines the generated timetable to further reduce conflicts and improve the overall quality.
- **Advanced Constraints**:
  - **Teacher-Course Pairing**: Ensures specific teachers are always paired with certain courses.
  - **Room and Teacher Conflicts**: Avoids scheduling multiple classes in the same room or assigning teachers to more than one course in the same timeslot.
  - **Teacher Workload Optimization**: Balances the number of courses assigned to each teacher, avoiding overloads.
- **Output Saved to File**: The final timetable is saved to a text file for easy access.

## **Installation**

To run this project, ensure that you have Python 3.x installed. You will also need to install the required dependencies.

### **Step 1: Clone the Repository**

Clone this repository to your local machine:

```bash
git clone https://github.com/kuladeep1906/Heuristic_search_project.git
cd Heuristic_Search_Project
```

### **Step 2: Install Required Dependencies**

Install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### **Step 3: Running the Project**

Run the `main.py` script to generate and refine the timetable:

```bash
python3 main.py
```

The program will:

1. Generate an initial timetable using a **Genetic Algorithm**.
2. Refine the timetable using **Real-Time A\*** to further optimize the solution.
3. Save the final timetable to a file called `final_timetable.txt`.

### **Example Command**:

```bash
python3 main.py
```

## **Usage**

After running the program, the final timetable will be saved to a text file named `final_timetable.txt` in the project directory. The format of the saved timetable will look something like this:

```plaintext
Final Timetable:
Course: Advanced Data Analytics, Room: Room 2, Teacher: Mr. A, Timeslot: 11 AM
Course: Artificial Intelligence, Room: Room 1, Teacher: Mr. A, Timeslot: 9 AM
Course: Business Analytics, Room: Room 3, Teacher: Ms. B, Timeslot: 11 AM
Course: Computer Science, Room: Room 3, Teacher: Mr. C, Timeslot: 12 PM
Course: Cyber Security, Room: Room 3, Teacher: Mr. C, Timeslot: 1 PM
Course: Data Science, Room: Room 2, Teacher: Ms. D, Timeslot: 10 AM
Course: Data Mining Machine Learning, Room: Room 5, Teacher: Ms. D, Timeslot: 1 PM
Course: Big Data Analytics, Room: Room 2, Teacher: Mr. E, Timeslot: 1 PM
Course: Heuristic Search, Room: Room 5, Teacher: Mr. E, Timeslot: 12 PM
Course: Real Time Systems, Room: Room 4, Teacher: Mr. E, Timeslot: 11 AM
Course: Reinforcement Learning, Room: Room 5, Teacher: Mr. F, Timeslot: 1 PM
Course: Machine Learning Design, Room: Room 4, Teacher: Mr. F, Timeslot: 12 PM
Course: Cloud Computing, Room: Room 4, Teacher: Mr. G, Timeslot: 10 AM
Course: Computer Networking, Room: Room 4, Teacher: Mr. G, Timeslot: 1 PM
```

## **Project Structure**

The project is structured as follows:

```
timetable-generator/
│
├── src/                  # Source code files
│   ├── main.py                 # Main script to run the timetable generator
│   ├── genetic_algorithm.py    # Genetic Algorithm implementation
│   ├── rta_star.py             # Real-Time A* Algorithm implementation
│   ├── fitness.py              # Fitness function and constraints
│   ├── timetable.py            # Timetable class definition
├── data/                       # Input data for courses, rooms, teachers
│   └── input_data.py           # Teacher, course, and timeslot data
├── requirements.txt            # Project dependencies
├── optimal_schedule.txt        # Final output with optimized timetable
└── README.md                   # Project documentation (this file)

optimal_schedule
```

## **Key Algorithms**

1. **Genetic Algorithm (GA)**:

   - A population-based optimization technique.
   - Uses crossover and mutation to evolve solutions over several generations.
   - Ensures valid schedules by checking room availability and teacher conflicts.

2. **Real-Time A\* (RTA\*)**:
   - A local optimization algorithm.
   - Refines the timetable produced by GA to improve the overall schedule by exploring neighbouring solutions.
   - Ensures minimal conflicts and adheres to specific teacher-course pairings.

## **Configuration**

You can modify the constraints, teacher-course pairings, room preferences, and more by editing the source files. For example:

- To change the **Teacher-Course Pairing** constraints, edit the `teacher_course_pairings` dictionary in `fitness.py`.

## **Further Development**

- Add additional constraints such as course sequence requirements or more complex room preferences.
- Visualize the generated timetable using a graphical interface.
- Integrate additional optimization techniques for better performance on larger datasets.
