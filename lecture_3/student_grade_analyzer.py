"""
Student Grade Analyzer
This program is designed for managing student lists and their grades.
It allows you to:
- Add new students
- Store and update the grade list
- Perform basic performance analysis
Usage:
Launch the program and follow the instructions in the menu.
"""

from math import floor

# List of students.
# Each element is a dictionary of the form:
# {'name': str, 'grades': list[int]}
students = []

error_message = (
    "Please check your input: the name must not be empty,"
    "and must be no less than 2 and no more than 50 characters long.\n"
    "The only permitted special characters are spaces, \"-\" or \"'\"."
)


def is_name_valid(name):
    """
    Checks the validity of a student's name.
    Conditions:
    - Name is not empty
    - Length from 2 to 50 characters
    - Acceptable characters: letters, spaces, hyphens, apostrophes
    Parameters:
    name (str): String containing the student's name
    Returns:
    bool: True if the name matches the rules, False otherwise
    """
    if not name or len(name) < 2 or len(name) > 50:
        return False
    if not all(ch.isalpha() or ch in [' ', '-', "'"] for ch in name):
        return False
    return True


def add_new_student():
    """
    Adds a new student to the `students` list.
    - Prompts the user for the student's name.
    - Checks if a student with that name exists: If so, displays a message and exits.
    - Checks the name's validity using the `is_name_valid` function.
    --If the name is valid, adds a dictionary of the form {'name': str, 'grades': []} to the students list.
    --If the name is invalid, displays an error message.
    -If an unexpected error occurs, displays a message with the exception text.
    Returns:
    None
    """
    try:
        name = input("Enter student name: ").strip(" -'")
        for student in students:
            if student['name'] == name:
                print(f"Student {name} already exists! Please, check your input.")
                return
        if is_name_valid(name):
            students.append(dict(name=name, grades=[]))
        else:
            print(f"Student {name} was not added.\n{error_message}")
    except Exception as err:
        print(f"Unexpected error while adding student: {err}")


def is_students_contains_name(students, name):
    """
    Checks if a student with the specified name is in the list.
    Used for the function add_new_grades().
    Parameters:
    students (list[dict]): a list of students, where each element is a dictionary {'name': str, 'grades': list[int]}
    name (str): the name of the student to search for
    Returns:
    bool: True if a student with that name is found, otherwise False
    """
    for student in students:
        if student['name'] == name:
            return True
    return False



def grade_process(student):
    """
    Requests grades for the specified student from the user and adds them to a list.
    Algorithm:
    1. The user enters a grade (a number between 0 and 100) or 'done' to complete the process.
    2. Each valid grade is added to the student['grades'] list.
    3. If an invalid value is entered:
    - ValueError: displays the message "Invalid input. Please enter a number."
    - TypeError: displays the message "Invalid input. Please enter a number between 0 and 100."
    4. The loop continues until the user enters 'done'.
    Parameters:
    student (dict): dictionary with keys 'name' (str) and 'grades' (list[int])
    Returns:
    None
    """
    grade = input("Enter a grade (or 'done' to finish): ").lower().strip(' ')
    while grade != 'done':
        try:
            if 0 <= int(grade) <= 100:
                student['grades'].append(int(grade))
            else:
                raise TypeError("Invalid input. Please enter a number between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except TypeError as exc:
            print(exc)
        grade = input("Enter a grade (or  'done' to finish): ").lower().strip(' ')


def add_new_grades():
    """
    Adds new grades for the selected student.
    Algorithm:
    1. Prompts the user for the student's name.
    2. Checks:
    - If the student list is empty or a student with that name is not found,
    displays a message and exits.
    3. If a student is found, calls the `grade_process(student)` function,
    which is responsible for entering and adding grades.
    Returns:
    None
    """
    name_student = input("Enter a student name to add grades: ")
    if len(students) == 0 or not is_students_contains_name(students, name_student):
        print("No student found. You can add a student by selecting menu item 1.")
        return
    for student in students:
        if student['name'] == name_student:
            grade_process(student)


def round_half_up(x, ndigits=0):
    """
    Rounds a number using the "round half up" rule.
    Parameters:
    x (float): number to round
    ndigits (int, optional): number of decimal places (default 0)
    Returns:
    float: rounded number
    """
    factor = 10 ** ndigits
    return floor(x * factor + 0.5) / factor


def generating_full_report():
    """
    Generates a complete student performance report.
    Algorithm:
    1. For each student:
    - Attempts to calculate the average grade (rounded according to the round_half_up rule).
    - If the student has no grades, displays "N/A".
    - Displays the student's name and average grade.
    2. Calculates:
    - Maximum average grade among all students.
    - Minimum average grade.
    - Overall average grade for all students.
    3. Displays the final report:
    - Max Average
    - Min Average
    - Overall Average
    4. If the student list is empty, displays a message indicating
    that students must be added first.
    Returns:
    None
    """
    print("--- Student Report ---")
    max_average = 0
    min_average = 100
    count_average = 0
    overall = 0
    try:
        for student in students:
            try:
                average_grade = round_half_up(sum(student['grades']) / len(student['grades']), 1)
                count_average += 1
                overall += average_grade
                max_average = max(max_average, average_grade)
                min_average = min(min_average, average_grade)
                print(f"{student['name']}'s average grade is {average_grade}.")
            except ZeroDivisionError:
                print(f"{student['name']}'s average grade is N/A.")

        overall_average = round_half_up(overall / count_average, 1)

        print('-' * 26)
        print(f"Max Average: {max_average}")
        print(f"Min Average: {min_average}")
        print(f"Overall Average: {overall_average}")
    except ZeroDivisionError:
        print("No student grades were found. " 
              "You can add a student by selecting menu item 1 and their grades by selecting menu item 2.")


def find_top_performer():
    """
    Finds the student with the highest GPA and displays the result.
    Algorithm:
    1. Uses the max() function to find the student with the highest GPA.
    - If the student has no grades, their GPA is assumed to be 0.
    2. If the found student has grades:
    - Calculates the GPA, rounding according to the round_half_up rule.
    - Displays the student's name and GPA.
    3. If the student has no grades:
    - Displays a message indicating that the best student has not been determined.
    4. If the student list is empty:
    - Handles ValueError and displays a message asking if more students need to be added.
    Returns:
    None
    """
    try:
        top_student = max(
            students,
            key=lambda student: sum(student['grades']) / len(student['grades']) if student['grades'] else 0)
        if top_student['grades']:
            average_grade = round_half_up(sum(top_student['grades']) / len(top_student['grades']), 1)
            print(f"The student with the highest average is {top_student['name']} with a grade of {average_grade}.")
        else:
            print("The best student is not determined, not enough grades. "
            "You can add grades to a student by selecting menu item 2.")
    except ValueError:
        print("No student found. You can add a student by selecting menu item 1.")



"""
Student Grade Analyzer main menu.
Functions:
1. Add a new student
2. Add grades to a student
3. Show a report for all students
4. Find the best student
5. Exit the program
The program runs in a loop until the user selects option 5.
All errors are caught and displayed as warnings.
"""
choice = ''   # variable for storing user choice
while choice != '5':   # the cycle continues until "Exit" is selected
    try:
        print('''--- Student Grade Analyser ---
1. Add a new student
2. Add grades for a student
3. Show report (all students)
4. Find top performer
5. Exit''')
        choice = input('Enter your choice: ').strip(' ')
        if choice == '1':
            add_new_student()
        elif choice == '2':
            add_new_grades()
        elif choice == '3':
            generating_full_report()
        elif choice == '4':
            find_top_performer()
        elif choice == '5':
            print("Good bye!")
        else:
            print("Invalid choice. Please, enter a number between 1 and 5")
    except Exception as e:
        print(f"Warning: {e}")
