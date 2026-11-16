# COMP 3005 - Assignment 3, Question 1

**Name:** Karman Sachar  
**Student ID:** 101285877

A Python application that connects to a PostgreSQL database and performs
CRUD (Create, Read, Update, Delete) operations on a `students` table.

## Demo Video

https://youtu.be/CX-ZidogybI

## Repository Structure

```
COMP3005_A3_Q1/
├── app/
│   └── students.py      Python application with the four CRUD functions
├── db/
│   └── schema.sql       Creates the students table and inserts the initial data
├── requirements.txt     Python dependency (psycopg2)
└── README.md
```

## Requirements

- PostgreSQL (tested with PostgreSQL 18) and pgAdmin 4
- Python 3.8 or newer
- The `psycopg2` library

## Setup

### 1. Create the database

1. Open pgAdmin 4 and connect to your PostgreSQL server.
2. Right-click **Databases**, choose **Create > Database...**, name it
   `students_db`, and click **Save**.

### 2. Create and populate the table

1. In pgAdmin, click `students_db`, then open **Tools > Query Tool**.
2. Open `db/schema.sql` (or paste its contents) and run it with **F5**.

This creates the `students` table and inserts the three initial students.
The script can be re-run at any time to reset the table.

### 3. Install the Python dependency

From the repository folder, run:

```
py -m pip install -r requirements.txt
```

(On macOS or Linux, use `python3` instead of `py`.)

### 4. Check the connection settings

The application connects with these default settings, defined at the top of
`app/students.py`:

| Setting  | Default       | Environment variable |
|----------|---------------|----------------------|
| Database | `students_db` | `PGDATABASE`         |
| User     | `postgres`    | `PGUSER`             |
| Password | `postgres`    | `PGPASSWORD`         |
| Host     | `localhost`   | `PGHOST`             |
| Port     | `5432`        | `PGPORT`             |

If your PostgreSQL password is different, either change the default in
`DB_CONFIG` or set the `PGPASSWORD` environment variable before running.

## Running the Application

The program is written in Python, so there is no compile step. From the
repository folder, run:

```
py app/students.py
```

A menu appears:

```
===== Students Menu =====
1. Get all students
2. Add a student
3. Update a student's email
4. Delete a student
5. Exit
```

Type a number and press Enter. Options 2, 3 and 4 ask for the values they
need.

## Functions

| Function | What it does |
|----------|--------------|
| `getAllStudents()` | Retrieves every record from the `students` table and prints them as a table, ordered by `student_id`. |
| `addStudent(first_name, last_name, email, enrollment_date)` | Inserts a new student and prints the `student_id` that was generated. Reports an error if the email is already in use. |
| `updateStudentEmail(student_id, new_email)` | Changes the email of the student with the given `student_id`. Reports if no such student exists or if the new email is already in use. |
| `deleteStudent(student_id)` | Deletes the student with the given `student_id`. Reports if no such student exists. |

All queries use parameterized statements, and each function handles database
errors (such as a failed connection or a duplicate email) by printing a clear
message instead of crashing.
