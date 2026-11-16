"""
COMP 3005 - Assignment 3, Question 1
PostgreSQL CRUD application for the students table.

Functions required by the assignment:
    getAllStudents()                                           - Read
    addStudent(first_name, last_name, email, enrollment_date)  - Create
    updateStudentEmail(student_id, new_email)                  - Update
    deleteStudent(student_id)                                  - Delete

Run with:  py app/students.py
"""

import os
from datetime import datetime

import psycopg2
from psycopg2 import errors

# ---------------------------------------------------------------------------
# Database connection settings.
# These defaults match the setup described in README.md. Each one can be
# overridden with an environment variable, so the password does not have to
# be edited in the code on another machine.
# ---------------------------------------------------------------------------
DB_CONFIG = {
    "dbname": os.environ.get("PGDATABASE", "students_db"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", "postgres"),
    "host": os.environ.get("PGHOST", "localhost"),
    "port": os.environ.get("PGPORT", "5432"),
}


def getConnection():
    """Opens and returns a new connection to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)


# ---------------------------------------------------------------------------
# CRUD functions
#
# Each function opens its own connection and always closes it in "finally".
# "with conn" commits the transaction if the block succeeds and rolls it
# back if an error is raised. All values are passed as %s parameters, so
# psycopg2 escapes them safely (this prevents SQL injection).
# ---------------------------------------------------------------------------
def getAllStudents():
    """Retrieves and displays all records from the students table."""
    conn = None
    try:
        conn = getConnection()
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT student_id, first_name, last_name, email, enrollment_date "
                "FROM students ORDER BY student_id;"
            )
            rows = cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error: could not retrieve students. {e}")
        return
    finally:
        if conn is not None:
            conn.close()

    if not rows:
        print("The students table is empty.")
        return

    # Print the records as a simple table.
    header = f"{'ID':<5}{'First Name':<15}{'Last Name':<15}{'Email':<32}{'Enrollment Date'}"
    print(header)
    print("-" * len(header))
    for student_id, first_name, last_name, email, enrollment_date in rows:
        date_text = str(enrollment_date) if enrollment_date else ""
        print(f"{student_id:<5}{first_name:<15}{last_name:<15}{email:<32}{date_text}")


def addStudent(first_name, last_name, email, enrollment_date):
    """Inserts a new student record into the students table."""
    conn = None
    try:
        conn = getConnection()
        with conn, conn.cursor() as cur:
            # RETURNING gives back the student_id generated for the new row.
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s) RETURNING student_id;",
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
        print(f"Added student {first_name} {last_name} with student_id {new_id}.")
    except errors.UniqueViolation:
        # The email column is UNIQUE, so a duplicate email is rejected.
        print(f"Error: a student with the email '{email}' already exists.")
    except psycopg2.Error as e:
        print(f"Error: could not add student. {e}")
    finally:
        if conn is not None:
            conn.close()


def updateStudentEmail(student_id, new_email):
    """Updates the email address of the student with the given student_id."""
    conn = None
    try:
        conn = getConnection()
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s;",
                (new_email, student_id),
            )
            updated = cur.rowcount  # number of rows changed (0 or 1)
        if updated == 0:
            print(f"No student found with student_id {student_id}.")
        else:
            print(f"Updated the email of student {student_id} to {new_email}.")
    except errors.UniqueViolation:
        print(f"Error: another student already uses the email '{new_email}'.")
    except psycopg2.Error as e:
        print(f"Error: could not update email. {e}")
    finally:
        if conn is not None:
            conn.close()


def deleteStudent(student_id):
    """Deletes the record of the student with the given student_id."""
    conn = None
    try:
        conn = getConnection()
        with conn, conn.cursor() as cur:
            cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
            deleted = cur.rowcount  # number of rows removed (0 or 1)
        if deleted == 0:
            print(f"No student found with student_id {student_id}.")
        else:
            print(f"Deleted student {student_id}.")
    except psycopg2.Error as e:
        print(f"Error: could not delete student. {e}")
    finally:
        if conn is not None:
            conn.close()


# ---------------------------------------------------------------------------
# Input helpers for the menu
# ---------------------------------------------------------------------------
def readText(prompt):
    """Asks until the user types something that is not blank."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def readStudentId(prompt):
    """Asks until the user types a whole number."""
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a whole number.")


def readDate(prompt):
    """Asks until the user types a valid date in YYYY-MM-DD format."""
    while True:
        value = input(prompt).strip()
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Please enter the date as YYYY-MM-DD, for example 2023-09-01.")


# ---------------------------------------------------------------------------
# Menu: lets the user call each function from the terminal
# ---------------------------------------------------------------------------
def main():
    """Shows a menu and calls the function the user picks."""
    while True:
        print("\n===== Students Menu =====")
        print("1. Get all students")
        print("2. Add a student")
        print("3. Update a student's email")
        print("4. Delete a student")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        print()

        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first_name = readText("First name: ")
            last_name = readText("Last name: ")
            email = readText("Email: ")
            enrollment_date = readDate("Enrollment date (YYYY-MM-DD): ")
            addStudent(first_name, last_name, email, enrollment_date)
        elif choice == "3":
            student_id = readStudentId("Student ID: ")
            new_email = readText("New email: ")
            updateStudentEmail(student_id, new_email)
        elif choice == "4":
            student_id = readStudentId("Student ID: ")
            deleteStudent(student_id)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
