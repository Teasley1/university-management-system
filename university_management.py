"""General University Management System - single inheritance and Tkinter GUI."""
import tkinter as tk
from tkinter import ttk, messagebox

COURSES = {
    "COMP 163 - Introduction to Programming": 3,
    "COMP 280 - Data Structures": 3,
    "COMP 350 - Operating Systems": 3,
    "COMP 365 - Artificial Intelligence": 3,
    "COMP 410 - Software Engineering": 3,
    "MATH 351 - Linear Algebra": 3,
}
GRADE_POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}


class Student:
    """Parent class holding shared student information and operations."""
    def __init__(self, first_name, last_name, student_id, phone, address):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.phone = phone
        self.address = address
        self.courses = {}  # course -> grade (None until assigned)

    def register_course(self, course):
        if course not in COURSES:
            raise ValueError("Choose a course from the available course list.")
        if course in self.courses:
            raise ValueError("This student is already registered for that course.")
        self.courses[course] = None

    def assign_grade(self, course, grade):
        if course not in self.courses:
            raise ValueError("The student must register for this course first.")
        if grade not in GRADE_POINTS:
            raise ValueError("Choose a valid letter grade.")
        self.courses[course] = grade

    def gpa(self):
        graded = [(COURSES[course], GRADE_POINTS[grade])
                  for course, grade in self.courses.items() if grade is not None]
        total_credits = sum(credits for credits, _ in graded)
        return (sum(credits * points for credits, points in graded) / total_credits
                if total_credits else None)

    def extra_info(self):
        return ""


class UndergraduateStudent(Student):
    """Undergraduate students register for courses only."""
    pass


class MSStudent(Student):
    """MS students can also register for an MS project."""
    def __init__(self, first_name, last_name, student_id, phone, address):
        super().__init__(first_name, last_name, student_id, phone, address)
        self.ms_project = None

    def register_ms_project(self, title):
        if not title.strip():
            raise ValueError("Enter an MS project title.")
        self.ms_project = title.strip()

    def extra_info(self):
        return f"MS Project: {self.ms_project or 'Not registered'}"


class PhDStudent(MSStudent):
    """PhD students inherit MS project registration and add a dissertation."""
    def __init__(self, first_name, last_name, student_id, phone, address):
        super().__init__(first_name, last_name, student_id, phone, address)
        self.dissertation = None

    def register_dissertation(self, title):
        if not title.strip():
            raise ValueError("Enter a dissertation title.")
        self.dissertation = title.strip()

    def extra_info(self):
        return f"{super().extra_info()}\nPhD Dissertation: {self.dissertation or 'Not registered'}"


class UniversityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("General University Management System")
        self.root.geometry("850x690")
        self.students = {}
        self.selected_id = tk.StringVar()
        self.student_type = tk.StringVar(value="Undergraduate")
        self.course_choice = tk.StringVar(value=list(COURSES)[0])
        self.grade_choice = tk.StringVar(value="A")
        self.fields = {}
        self.build_gui()

    def build_gui(self):
        outer = ttk.Frame(self.root, padding=14)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="General University Management System",
                  font=("Arial", 17, "bold")).pack(anchor="w", pady=(0, 10))
        notebook = ttk.Notebook(outer)
        notebook.pack(fill="both", expand=True)
        add_tab = ttk.Frame(notebook, padding=12)
        manage_tab = ttk.Frame(notebook, padding=12)
        notebook.add(add_tab, text="Add Student")
        notebook.add(manage_tab, text="Manage Students")

        for row, (key, label) in enumerate([
            ("first_name", "First name"), ("last_name", "Last name"),
            ("student_id", "Student ID"), ("phone", "Phone number"),
            ("address", "Address")]):
            ttk.Label(add_tab, text=label).grid(row=row, column=0, sticky="w", pady=6)
            entry = ttk.Entry(add_tab, width=43)
            entry.grid(row=row, column=1, sticky="w", padx=10, pady=6)
            self.fields[key] = entry
        ttk.Label(add_tab, text="Student type").grid(row=5, column=0, sticky="w", pady=6)
        ttk.Combobox(add_tab, textvariable=self.student_type, state="readonly", width=40,
                     values=["Undergraduate", "MS", "PhD"]).grid(row=5, column=1, padx=10, sticky="w")
        ttk.Button(add_tab, text="Add Student", command=self.add_student).grid(
            row=6, column=1, sticky="w", padx=10, pady=15)

        ttk.Label(manage_tab, text="Select student").grid(row=0, column=0, sticky="w")
        self.student_picker = ttk.Combobox(manage_tab, textvariable=self.selected_id,
                                           state="readonly", width=49)
        self.student_picker.grid(row=0, column=1, columnspan=2, sticky="w", padx=8)
        self.student_picker.bind("<<ComboboxSelected>>", lambda _event: self.view_student())
        ttk.Label(manage_tab, text="Available courses").grid(row=1, column=0, sticky="w", pady=9)
        ttk.Combobox(manage_tab, textvariable=self.course_choice, state="readonly", width=49,
                     values=list(COURSES)).grid(row=1, column=1, columnspan=2, sticky="w", padx=8)
        ttk.Button(manage_tab, text="Register Course", command=self.register_course).grid(
            row=2, column=0, sticky="w", pady=5)
        ttk.Button(manage_tab, text="Show Available Courses", command=self.show_courses).grid(
            row=2, column=1, sticky="w", padx=8)
        ttk.Button(manage_tab, text="Show Registered Courses", command=self.show_registered).grid(
            row=3, column=0, sticky="w", pady=5)
        ttk.Button(manage_tab, text="View Student Information", command=self.view_student).grid(
            row=3, column=1, sticky="w", padx=8)
        ttk.Label(manage_tab, text="Grade").grid(row=4, column=0, sticky="w", pady=8)
        ttk.Combobox(manage_tab, textvariable=self.grade_choice, state="readonly", width=10,
                     values=list(GRADE_POINTS)).grid(row=4, column=1, sticky="w", padx=8)
        ttk.Button(manage_tab, text="Assign Grade to Selected Course", command=self.assign_grade).grid(
            row=5, column=0, columnspan=2, sticky="w", pady=4)
        ttk.Label(manage_tab, text="MS project / dissertation title").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(12, 4))
        self.project_title = ttk.Entry(manage_tab, width=53)
        self.project_title.grid(row=7, column=0, columnspan=3, sticky="w")
        ttk.Button(manage_tab, text="Register MS Project", command=self.register_project).grid(
            row=8, column=0, sticky="w", pady=8)
        ttk.Button(manage_tab, text="Register PhD Dissertation", command=self.register_dissertation).grid(
            row=8, column=1, sticky="w", padx=8)
        self.output = tk.Text(manage_tab, width=92, height=14, wrap="word", state="disabled")
        self.output.grid(row=9, column=0, columnspan=3, sticky="nsew", pady=8)
        manage_tab.rowconfigure(9, weight=1)
        manage_tab.columnconfigure(2, weight=1)

    def write_output(self, message):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", message)
        self.output.configure(state="disabled")

    def add_student(self):
        data = {key: entry.get().strip() for key, entry in self.fields.items()}
        if not all(data.values()):
            messagebox.showerror("Missing information", "Please complete every student field.")
            return
        if data["student_id"] in self.students:
            messagebox.showerror("Duplicate ID", "A student with this ID already exists.")
            return
        cls = {"Undergraduate": UndergraduateStudent, "MS": MSStudent,
               "PhD": PhDStudent}[self.student_type.get()]
        student = cls(**data)
        self.students[student.student_id] = student
        self.student_picker["values"] = [
            f"{s.student_id} - {s.first_name} {s.last_name}" for s in self.students.values()]
        self.selected_id.set(f"{student.student_id} - {student.first_name} {student.last_name}")
        for entry in self.fields.values():
            entry.delete(0, "end")
        messagebox.showinfo("Student added", f"Added {student.first_name} {student.last_name}.")
        self.view_student()

    def current_student(self):
        student_id = self.selected_id.get().split(" - ")[0]
        student = self.students.get(student_id)
        if student is None:
            messagebox.showwarning("Select student", "Please add and select a student first.")
        return student

    def student_header(self, student):
        return (f"Name: {student.first_name} {student.last_name}\n"
                f"Student ID: {student.student_id}\n")

    def show_courses(self):
        self.write_output("AVAILABLE COURSES\n\n" + "\n".join(
            f"{course} ({credits} credits)" for course, credits in COURSES.items()))

    def show_registered(self):
        student = self.current_student()
        if student is None:
            return
        courses = "\n".join(f"{course} | Grade: {grade or 'Not assigned'}"
                            for course, grade in student.courses.items()) or "None"
        self.write_output(self.student_header(student) + "\nREGISTERED COURSES\n" + courses)

    def view_student(self):
        student = self.current_student()
        if student is None:
            return
        gpa = student.gpa()
        courses = "\n".join(f"- {course} | Grade: {grade or 'Not assigned'}"
                            for course, grade in student.courses.items()) or "None"
        extra = student.extra_info()
        gpa_text = f"{gpa:.2f}" if gpa is not None else "N/A"
        self.write_output(
            self.student_header(student)
            + f"Type: {type(student).__name__}\nPhone: {student.phone}\n"
            + f"Address: {student.address}\nGPA: {gpa_text}\n"
        )
        # Append course and optional project information to the personal details.
        self.output.configure(state="normal")
        self.output.insert("end", f"\nRegistered courses:\n{courses}\n")
        if extra:
            self.output.insert("end", f"\n{extra}\n")
        self.output.configure(state="disabled")

    def register_course(self):
        student = self.current_student()
        if student is None:
            return
        try:
            student.register_course(self.course_choice.get())
        except ValueError as error:
            messagebox.showerror("Registration error", str(error))
            return
        self.show_registered()

    def assign_grade(self):
        student = self.current_student()
        if student is None:
            return
        try:
            student.assign_grade(self.course_choice.get(), self.grade_choice.get())
        except ValueError as error:
            messagebox.showerror("Grade error", str(error))
            return
        self.view_student()

    def register_project(self):
        student = self.current_student()
        if student is None:
            return
        if not isinstance(student, MSStudent):
            messagebox.showerror("Not eligible", "Only MS and PhD students can register for an MS project.")
            return
        try:
            student.register_ms_project(self.project_title.get())
        except ValueError as error:
            messagebox.showerror("Project error", str(error))
            return
        self.view_student()

    def register_dissertation(self):
        student = self.current_student()
        if student is None:
            return
        if not isinstance(student, PhDStudent):
            messagebox.showerror("Not eligible", "Only PhD students can register for a dissertation.")
            return
        try:
            student.register_dissertation(self.project_title.get())
        except ValueError as error:
            messagebox.showerror("Dissertation error", str(error))
            return
        self.view_student()


def main():
    root = tk.Tk()
    UniversityApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
