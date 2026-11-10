GENERAL UNIVERSITY MANAGEMENT SYSTEM

Run:
  python3 university_management.py

Uses Python 3 and Tkinter (standard library on many Python installations).
If your Python installation does not include Tkinter, install a Python distribution with Tk support.

How to test:
1. Add an Undergraduate student in the Add Student tab.
2. Go to Manage Students and select the student.
3. Show available courses, choose a course, then Register Course.
4. Show Registered Courses; confirm name, ID and course appear.
5. Assign a grade to the selected course and view the updated GPA.
6. Add an MS student and register an MS project.
7. Add a PhD student and register an MS project and dissertation.
8. Confirm an undergraduate cannot register an MS project or dissertation.

Inheritance:
Student is the base class. UndergraduateStudent and MSStudent inherit Student.
PhDStudent inherits MSStudent, which in turn inherits Student. Each class
has exactly one direct parent class (single inheritance).

Data is held in memory while the application is running; it is not saved to disk.
