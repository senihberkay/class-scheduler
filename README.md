# Class Scheduler

A web-based class scheduling tool built using Streamlit, designed specifically for Özyeğin University students. This application allows users to select courses, view class sections, and visualize their weekly timetable in an organized and visually appealing table format. The tool also provides a conflict detection mechanism to avoid schedule clashes.

&ensp;

## Motivation

This project was created to make the course registration process easier for my brother who is newly enrolled in Özyeğin University.

&ensp;

## Features

- **Search Courses:** Easily search for courses using the sidebar with a built-in search functionality.
- **Course Section Information:** View detailed information about each course section, including the instructor and the session's time range.
- **Color-Coded Schedule:** Each course is assigned a unique color to improve readability and organization.
- **Conflict Detection:** The application detects scheduling conflicts and notifies users when two or more classes overlap.

&ensp;

## How It Works

1. **Course Selection:**
   - In the sidebar, users can search and select courses they are enrolled in.
   - For each course, users can select the desired section, which will display the instructor’s name and the class timings.
   
2. **Generating Schedule:**
   - Once the courses and sections are selected, the tool generates a weekly timetable in a clear table format, highlighting the course section codes instead of just the course codes.
   
3. **Conflict Detection:**
   - If there are any schedule conflicts between selected courses, the user is notified with an error message.

&ensp;

## Project Structure

```plaintext
├── courses.csv            # CSV file containing course and section information.
├── app.py                 # Main Streamlit application code.
├── utils.py               # Utility functions for schedule generation.
├── README.md              # Project documentation.
├── .gitignore             # Git ignore file.
├── requirements.txt       # Dependencies for the project.
```

&ensp;

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/senihberkay/class-scheduler.git
   cd class-scheduler
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   
3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

&ensp;

## Future Improvements

- Adding more customizable views for the schedule (e.g., daily view).
- A search button to filter courses in the sidebar.
- Exporting the schedule to PDF or other formats.
- Allow users to import course data from external sources such as CSV, Excel, or JSON files.

&ensp;

## Contributing

Feel free to fork this repository and create pull requests to contribute to the development of Class Scheduler. If you want to create a similar programming site with your data, you can start using the project by updating the courses.csv file with your own course information.

&ensp;
