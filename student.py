import os

# --- Constants ---
DATA_FILE = "students.txt"

# --- 1. Class Definition (Concept: Class, Object) ---
class Student:
    """Represents a student with an ID, name, and marks."""
    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = marks # Stored as a dictionary: {'subject': score}

    def calculate_average(self):
        """Calculates the average mark for the student."""
        if not self.marks:
            return 0
        total = sum(self.marks.values())
        return total / len(self.marks)

    def to_dict(self):
        """Returns student data as a dictionary for file saving."""
        return {
            'id': self.student_id,
            'name': self.name,
            'marks': self.marks
        }

    @staticmethod
    def from_dict(data):
        """Creates a Student object from a dictionary."""
        return Student(data['id'], data['name'], data['marks'])

    def __str__(self):
        """String representation for viewing student details."""
        avg = self.calculate_average()
        marks_str = ", ".join([f"{k}: {v}" for k, v in self.marks.items()])
        return (f"ID: {self.student_id}, Name: {self.name}, "
                f"Marks: {{{marks_str}}}, Average: {avg:.2f}")

# --- 2. File Handling Functions (Concept: File Handling) ---

def load_students():
    """Loads student data from the file (students.txt)."""
    students = {} # Concept: Dictionary (to store students by ID)
    if not os.path.exists(DATA_FILE):
        return students

    try:
        with open(DATA_FILE, 'r') as f:
            for line in f:
                # Basic parsing: ID,Name,Subject1=Score1;Subject2=Score2
                try:
                    parts = line.strip().split(',', 2)
                    student_id = parts[0]
                    name = parts[1]
                    marks_data = parts[2].split(';') if len(parts) > 2 else []

                    marks = {} # Concept: Dictionary
                    for item in marks_data:
                        if '=' in item:
                            subj, score = item.split('=')
                            marks[subj.strip()] = int(score.strip())

                    student = Student(student_id, name, marks)
                    students[student_id] = student

                except (ValueError, IndexError) as e:
                    print(f"**Error**: Corrupt data line skipped: {line.strip()}. Error: {e}")
        return students

    except IOError as e: # Concept: Exception Handling
        print(f"**Error**: Could not read from file {DATA_FILE}: {e}")
        return students


def save_students(students):
    """Saves student data to the file (students.txt)."""
    try:
        with open(DATA_FILE, 'w') as f:
            for student in students.values():
                # Format: ID,Name,Subject1=Score1;Subject2=Score2
                marks_str = ";".join([f"{k}={v}" for k, v in student.marks.items()])
                f.write(f"{student.student_id},{student.name},{marks_str}\n")
        print(f"Data saved successfully to {DATA_FILE}.")
    except IOError as e: # Concept: Exception Handling
        print(f"**Error**: Could not write to file {DATA_FILE}: {e}")

# --- 3. Management Functions (Concept: Functions, Loops, Condition) ---

def add_new_student(students):
    """Feature: New Student - add"""
    print("\n--- Add New Student ---")
    while True: # Concept: Loop
        student_id = input("Enter Student ID (e.g., S101): ").strip()
        if student_id in students: # Concept: Condition
            print(f"Error: Student ID {student_id} already exists. Please use a unique ID.")
        else:
            break

    name = input("Enter Student Name: ").strip().title()

    marks = {} # Concept: Dictionary
    print("Enter marks (Subject Name and Score). Type 'done' to finish.")
    while True: # Concept: Loop
        subject = input("Enter Subject Name (or 'done'): ").strip().title()
        if subject.lower() == 'done':
            break

        try:
            score = int(input(f"Enter Score for {subject}: "))
            if 0 <= score <= 100: # Concept: Condition
                marks[subject] = score
            else:
                print("Score must be between 0 and 100.")
        except ValueError: # Concept: Exception Handling
            print("Invalid input. Please enter a number for the score.")

    new_student = Student(student_id, name, marks) # Concept: Object creation
    students[student_id] = new_student
    print(f"Student {name} added successfully.")
    save_students(students)


def view_all_students(students):
    """Feature: View all students"""
    print("\n--- All Registered Students ---")
    if not students:
        print("No students registered yet.")
        return

    for student in students.values(): # Concept: Loop
        print(str(student))


def students_search(students):
    """Feature: Students search"""
    print("\n--- Student Search ---")
    search_id = input("Enter Student ID to search: ").strip()

    if search_id in students: # Concept: Condition
        student = students[search_id]
        print("\n**Student Found**")
        print(str(student))
    else: # Concept: Condition
        print(f"Error: Student with ID {search_id} not found.")


def update_and_delete_student(students):
    """Feature: Update and Delete"""
    print("\n--- Update or Delete Student ---")
    student_id = input("Enter Student ID to update or delete: ").strip()

    if student_id not in students: # Concept: Condition
        print(f"Error: Student with ID {student_id} not found.")
        return

    student = students[student_id]
    print(f"\nCurrently viewing: {student.name}")
    print("What do you want to do?")
    print("1. Update Marks")
    print("2. Delete Student")
    choice = input("Enter choice (1/2): ").strip()

    if choice == '1':
        print("\n--- Update Marks ---")
        subject = input("Enter Subject Name to update/add: ").strip().title()
        try:
            score = int(input(f"Enter new score for {subject}: "))
            if 0 <= score <= 100:
                student.marks[subject] = score # Concept: Dictionary modification
                print(f"Marks for {subject} updated/added successfully.")
                save_students(students)
            else:
                print("Score must be between 0 and 100.")
        except ValueError: # Concept: Exception Handling
            print("Invalid input. Please enter a number for the score.")

    elif choice == '2':
        confirm = input(f"Are you sure you want to DELETE {student.name}? (yes/no): ").lower().strip()
        if confirm == 'yes': # Concept: Condition
            del students[student_id]
            print(f"Student {student_id} deleted successfully.")
            save_students(students)
        else:
            print("Deletion cancelled.")

    else:
        print("Invalid choice.")


def calculate_avg_and_find_topper(students):
    """Feature: Calculate avg & find topper"""
    print("\n--- Calculate Averages and Find Topper ---")
    if not students:
        print("No students registered to calculate averages.")
        return

    topper = None
    highest_avg = -1

    print("\n**Student Averages**")
    for student in students.values(): # Concept: Loop
        avg = student.calculate_average()
        print(f"ID: {student.student_id}, Name: {student.name}, Average: {avg:.2f}")

        if avg > highest_avg: # Concept: Condition
            highest_avg = avg
            topper = student
        elif avg == highest_avg and topper and student.student_id != topper.student_id:
             # Handle ties if needed, but for simplicity, the first found is often the "topper"
             pass

    if topper:
        print("\n**🎉 Class Topper 🎉**")
        print(f"Name: {topper.name}, Highest Average: {highest_avg:.2f}")

# --- 4. Main Program Loop ---

def main():
    """Main function to run the Student Management System."""
    print("--- 🎓 Welcome to Student Management System 🎓 ---")
    students = load_students() # Load data at startup

    while True: # Concept: Loop (Main Menu Loop)
        print("\n--- Main Menu ---")
        print("1. New Student - Add")
        print("2. View All Students")
        print("3. Students Search")
        print("4. Update and Delete Student")
        print("5. Calculate Avg & Find Topper")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        # Concept: Condition (for menu selection)
        if choice == '1':
            add_new_student(students)
        elif choice == '2':
            view_all_students(students)
        elif choice == '3':
            students_search(students)
        elif choice == '4':
            update_and_delete_student(students)
        elif choice == '5':
            calculate_avg_and_find_topper(students)
        elif choice == '6':
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            # Concept: Exception Handling (handled by the invalid choice message)

# --- Execute Main Function ---
if __name__ == "__main__":
    main()