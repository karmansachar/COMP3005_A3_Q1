-- COMP 3005 - Assignment 3, Question 1
-- Creates the students table and inserts the initial data.
--
-- Run this script inside the students_db database (see README.md).
-- It can be re-run at any time to reset the table to its starting state.

-- Remove the old table (if any) so the script always starts clean.
DROP TABLE IF EXISTS students;

-- students table, as given in the assignment schema.
CREATE TABLE students (
    student_id      SERIAL PRIMARY KEY,     -- Integer, primary key, auto-increment
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

-- Initial data, as given in the assignment.
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
