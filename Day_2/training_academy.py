# ==========================================================
# Student Training Academy Database Management System
# ==========================================================

# ==========================================================
# Import Required Libraries
# ==========================================================

# Import SQLite library
import sqlite3

# Import Pandas library
import pandas as pd


# ==========================================================
# Helper Function: Connect to Database
# ==========================================================

def connect_db(db_name):

    # Create SQLite database connection
    conn = sqlite3.connect(db_name)

    # Enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON;")

    # Return connection object
    return conn


# ==========================================================
# Helper Function: Execute SQL Query
# ==========================================================

def execute_query(conn, sql, params=None):

    # Check whether parameters are passed
    if params is None:
        params = []

    # Execute SQL query
    cursor = conn.execute(sql, params)

    # Save changes permanently
    conn.commit()

    # Return cursor object
    return cursor


# ==========================================================
# Helper Function: Read SQL Query
# ==========================================================

def read_query(conn, sql, params=None):

    # Check whether parameters are passed
    if params is None:
        params = []

    # Execute SELECT query and return DataFrame
    return pd.read_sql_query(sql, conn, params=params)


# ==========================================================
# Task 1: Create SQLite Database Using Python
# ==========================================================

# Objective:
# Create a SQLite database named training_academy.db
# and enable foreign key support.

# Create database connection
conn = connect_db("training_academy.db")

# Create cursor object
cursor = conn.cursor()

# Display success message
print("Database created successfully.")

# ==========================================================
# Task 2: Create Tables
# ==========================================================

# ----------------------------------------------------------
# Create Departments Table
# ----------------------------------------------------------

# SQL query to create departments table
create_departments_table = """
CREATE TABLE IF NOT EXISTS departments(

    department_id INTEGER PRIMARY KEY,

    department_name TEXT NOT NULL UNIQUE

);
"""

# Execute the SQL query
execute_query(conn, create_departments_table)

print("Departments table created successfully.")


# ----------------------------------------------------------
# Create Students Table
# ----------------------------------------------------------

# SQL query to create students table
create_students_table = """
CREATE TABLE IF NOT EXISTS students(

    student_id INTEGER PRIMARY KEY,

    student_name TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    city TEXT,

    registration_date DATE NOT NULL

);
"""

# Execute the SQL query
execute_query(conn, create_students_table)

print("Students table created successfully.")


# ----------------------------------------------------------
# Create Instructors Table
# ----------------------------------------------------------

# SQL query to create instructors table
create_instructors_table = """
CREATE TABLE IF NOT EXISTS instructors(

    instructor_id INTEGER PRIMARY KEY,

    instructor_name TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    department_id INTEGER,

    FOREIGN KEY(department_id)
    REFERENCES departments(department_id)

);
"""

# Execute the SQL query
execute_query(conn, create_instructors_table)

print("Instructors table created successfully.")


# ----------------------------------------------------------
# Create Courses Table
# ----------------------------------------------------------

# SQL query to create courses table
create_courses_table = """
CREATE TABLE IF NOT EXISTS courses(

    course_id INTEGER PRIMARY KEY,

    course_name TEXT NOT NULL,

    department_id INTEGER,

    instructor_id INTEGER,

    fee REAL NOT NULL CHECK(fee >= 0),

    level TEXT CHECK(level IN ('Beginner','Intermediate','Advanced')),

    FOREIGN KEY(department_id)
    REFERENCES departments(department_id),

    FOREIGN KEY(instructor_id)
    REFERENCES instructors(instructor_id)

);
"""

# Execute the SQL query
execute_query(conn, create_courses_table)

print("Courses table created successfully.")


# ----------------------------------------------------------
# Create Enrollments Table
# ----------------------------------------------------------

# SQL query to create enrollments table
create_enrollments_table = """
CREATE TABLE IF NOT EXISTS enrollments(

    enrollment_id INTEGER PRIMARY KEY,

    student_id INTEGER,

    course_id INTEGER,

    enrollment_date DATE NOT NULL,

    status TEXT DEFAULT 'Active'
    CHECK(status IN ('Active','Completed','Cancelled')),

    UNIQUE(student_id, course_id),

    FOREIGN KEY(student_id)
    REFERENCES students(student_id),

    FOREIGN KEY(course_id)
    REFERENCES courses(course_id)

);
"""

# Execute the SQL query
execute_query(conn, create_enrollments_table)

print("Enrollments table created successfully.")


# ----------------------------------------------------------
# Create Payments Table
# ----------------------------------------------------------

# SQL query to create payments table
create_payments_table = """
CREATE TABLE IF NOT EXISTS payments(

    payment_id INTEGER PRIMARY KEY,

    enrollment_id INTEGER UNIQUE,

    amount REAL NOT NULL CHECK(amount >= 0),

    payment_date DATE NOT NULL,

    payment_status TEXT
    CHECK(payment_status IN ('Paid','Pending','Refunded')),

    FOREIGN KEY(enrollment_id)
    REFERENCES enrollments(enrollment_id)

);
"""

# Execute the SQL query
execute_query(conn, create_payments_table)

print("Payments table created successfully.")


# ==========================================================
# Task 3: Insert Sample Data
# ==========================================================

# ----------------------------------------------------------
# Insert Data into Departments Table
# ----------------------------------------------------------

# SQL query to insert department records
insert_departments = """
INSERT OR IGNORE INTO departments
(department_id, department_name)
VALUES
(?, ?);
"""

# Insert Department 1
execute_query(conn, insert_departments, (1, "Data Science"))

# Insert Department 2
execute_query(conn, insert_departments, (2, "Software Engineering"))

# Insert Department 3
execute_query(conn, insert_departments, (3, "Business Analytics"))

print("Department records inserted successfully.")


# ----------------------------------------------------------
# Insert Data into Students Table
# ----------------------------------------------------------

# SQL query to insert student records
insert_students = """
INSERT OR IGNORE INTO students
(student_id, student_name, email, city, registration_date)
VALUES
(?, ?, ?, ?, ?);
"""

execute_query(conn, insert_students,
              (1, "Rahul Kumar", "rahul.kumar@example.com", "Patna", "2026-01-05"))

execute_query(conn, insert_students,
              (2, "Priya Singh", "priya.singh@example.com", "Kolkata", "2026-01-06"))

execute_query(conn, insert_students,
              (3, "Amit Raj", "amit.raj@example.com", "Delhi", "2026-01-07"))

execute_query(conn, insert_students,
              (4, "Sneha Verma", "sneha.verma@example.com", "Patna", "2026-01-10"))

execute_query(conn, insert_students,
              (5, "Aditya Sharma", "aditya.sharma@example.com", "Mumbai", "2026-01-12"))

print("Student records inserted successfully.")


# ----------------------------------------------------------
# Insert Data into Instructors Table
# ----------------------------------------------------------

# SQL query to insert instructor records
insert_instructors = """
INSERT OR IGNORE INTO instructors
(instructor_id, instructor_name, email, department_id)
VALUES
(?, ?, ?, ?);
"""

execute_query(conn, insert_instructors,
              (1, "Dr. Meera Iyer", "meera.iyer@example.com", 1))

execute_query(conn, insert_instructors,
              (2, "Arjun Sen", "arjun.sen@example.com", 2))

execute_query(conn, insert_instructors,
              (3, "Kavita Rao", "kavita.rao@example.com", 3))

print("Instructor records inserted successfully.")


# ----------------------------------------------------------
# Insert Data into Courses Table
# ----------------------------------------------------------

# SQL query to insert course records
insert_courses = """
INSERT OR IGNORE INTO courses
(course_id, course_name, department_id, instructor_id, fee, level)
VALUES
(?, ?, ?, ?, ?, ?);
"""

execute_query(conn, insert_courses,
              (101, "Python for Beginners", 2, 2, 4999, "Beginner"))

execute_query(conn, insert_courses,
              (102, "SQL and RDBMS Masterclass", 1, 1, 6999, "Beginner"))

execute_query(conn, insert_courses,
              (103, "Machine Learning Basics", 1, 1, 11999, "Intermediate"))

execute_query(conn, insert_courses,
              (104, "Business Dashboarding", 3, 3, 8999, "Intermediate"))

execute_query(conn, insert_courses,
              (105, "Advanced Data Engineering", 1, 1, 15999, "Advanced"))

print("Course records inserted successfully.")


# ----------------------------------------------------------
# Insert Data into Enrollments Table
# ----------------------------------------------------------

# SQL query to insert enrollment records
insert_enrollments = """
INSERT OR IGNORE INTO enrollments
(enrollment_id, student_id, course_id, enrollment_date, status)
VALUES
(?, ?, ?, ?, ?);
"""

execute_query(conn, insert_enrollments,
              (1001, 1, 101, "2026-02-01", "Active"))

execute_query(conn, insert_enrollments,
              (1002, 1, 102, "2026-02-03", "Completed"))

execute_query(conn, insert_enrollments,
              (1003, 2, 102, "2026-02-04", "Active"))

execute_query(conn, insert_enrollments,
              (1004, 3, 103, "2026-02-05", "Active"))

execute_query(conn, insert_enrollments,
              (1005, 4, 104, "2026-02-07", "Cancelled"))

print("Enrollment records inserted successfully.")


# ----------------------------------------------------------
# Insert Data into Payments Table
# ----------------------------------------------------------

# SQL query to insert payment records
insert_payments = """
INSERT OR IGNORE INTO payments
(payment_id, enrollment_id, amount, payment_date, payment_status)
VALUES
(?, ?, ?, ?, ?);
"""

execute_query(conn, insert_payments,
              (501, 1001, 4999, "2026-02-01", "Paid"))

execute_query(conn, insert_payments,
              (502, 1002, 6999, "2026-02-03", "Paid"))

execute_query(conn, insert_payments,
              (503, 1003, 6999, "2026-02-04", "Pending"))

execute_query(conn, insert_payments,
              (504, 1004, 11999, "2026-02-05", "Paid"))

execute_query(conn, insert_payments,
              (505, 1005, 0, "2026-02-07", "Refunded"))

print("Payment records inserted successfully.")


# ==========================================================
# Task 4: Display All Tables
# ==========================================================

# ----------------------------------------------------------
# Display Departments Table
# ----------------------------------------------------------

print("\n================ Departments Table ================\n")

departments_df = read_query(conn, "SELECT * FROM departments")

print(departments_df)


# ----------------------------------------------------------
# Display Students Table
# ----------------------------------------------------------

print("\n================ Students Table ================\n")

students_df = read_query(conn, "SELECT * FROM students")

print(students_df)


# ----------------------------------------------------------
# Display Instructors Table
# ----------------------------------------------------------

print("\n================ Instructors Table ================\n")

instructors_df = read_query(conn, "SELECT * FROM instructors")

print(instructors_df)


# ----------------------------------------------------------
# Display Courses Table
# ----------------------------------------------------------

print("\n================ Courses Table ================\n")

courses_df = read_query(conn, "SELECT * FROM courses")

print(courses_df)


# ----------------------------------------------------------
# Display Enrollments Table
# ----------------------------------------------------------

print("\n================ Enrollments Table ================\n")

enrollments_df = read_query(conn, "SELECT * FROM enrollments")

print(enrollments_df)


# ----------------------------------------------------------
# Display Payments Table
# ----------------------------------------------------------

print("\n================ Payments Table ================\n")

payments_df = read_query(conn, "SELECT * FROM payments")

print(payments_df)


# ==========================================================
# Task 5: Basic SQL Queries
# ==========================================================

# ----------------------------------------------------------
# Query 1: Show All Students
# ----------------------------------------------------------

print("\n========== Query 1: Show All Students ==========\n")

query1 = """
SELECT *
FROM students;
"""

print(read_query(conn, query1))


# ----------------------------------------------------------
# Query 2: Show Student Name, Email and City
# ----------------------------------------------------------

print("\n========== Query 2: Student Name, Email and City ==========\n")

query2 = """
SELECT student_name,
       email,
       city
FROM students;
"""

print(read_query(conn, query2))


# ----------------------------------------------------------
# Query 3: Show Students From Patna
# ----------------------------------------------------------

print("\n========== Query 3: Students From Patna ==========\n")

query3 = """
SELECT *
FROM students
WHERE city = 'Patna';
"""

print(read_query(conn, query3))


# ----------------------------------------------------------
# Query 4: Show Courses With Fee Greater Than 7000
# ----------------------------------------------------------

print("\n========== Query 4: Courses With Fee Greater Than 7000 ==========\n")

query4 = """
SELECT *
FROM courses
WHERE fee > 7000;
"""

print(read_query(conn, query4))


# ----------------------------------------------------------
# Query 5: Show Beginner Level Courses
# ----------------------------------------------------------

print("\n========== Query 5: Beginner Level Courses ==========\n")

query5 = """
SELECT *
FROM courses
WHERE level = 'Beginner';
"""

print(read_query(conn, query5))


# ----------------------------------------------------------
# Query 6: Show Students Sorted By Name
# ----------------------------------------------------------

print("\n========== Query 6: Students Sorted By Name ==========\n")

query6 = """
SELECT *
FROM students
ORDER BY student_name ASC;
"""

print(read_query(conn, query6))


# ----------------------------------------------------------
# Query 7: Show Top 3 Highest Fee Courses
# ----------------------------------------------------------

print("\n========== Query 7: Top 3 Highest Fee Courses ==========\n")

query7 = """
SELECT course_name,
       fee
FROM courses
ORDER BY fee DESC
LIMIT 3;
"""

print(read_query(conn, query7))


# ----------------------------------------------------------
# Query 8: Show Distinct Student Cities
# ----------------------------------------------------------

print("\n========== Query 8: Distinct Student Cities ==========\n")

query8 = """
SELECT DISTINCT city
FROM students;
"""

print(read_query(conn, query8))


# ----------------------------------------------------------
# Query 9: Show Pending Payments
# ----------------------------------------------------------

print("\n========== Query 9: Pending Payments ==========\n")

query9 = """
SELECT *
FROM payments
WHERE payment_status = 'Pending';
"""

print(read_query(conn, query9))


# ----------------------------------------------------------
# Query 10: Show Active Enrollments
# ----------------------------------------------------------

print("\n========== Query 10: Active Enrollments ==========\n")

query10 = """
SELECT *
FROM enrollments
WHERE status = 'Active';
"""

print(read_query(conn, query10))


# ==========================================================
# Task 6: INSERT Operation Using Python
# ==========================================================

# ----------------------------------------------------------
# Insert New Student Record
# ----------------------------------------------------------

# SQL query to insert a new student
insert_new_student = """
INSERT INTO students
(student_id, student_name, email, city, registration_date)
VALUES
(?, ?, ?, ?, ?);
"""

# Store new student details
new_student = (
    6,
    "Rohan Das",
    "rohan.das@example.com",
    "Pune",
    "2026-02-15"
)

# Execute insert query
execute_query(conn, insert_new_student, new_student)

print("New student inserted successfully.")


# ----------------------------------------------------------
# Display Newly Inserted Student
# ----------------------------------------------------------

print("\n========== Newly Inserted Student ==========\n")

display_student = """
SELECT *
FROM students
WHERE student_id = 6;
"""

print(read_query(conn, display_student))


# ==========================================================
# Task 7: UPDATE Operation Using Python
# ==========================================================

# ----------------------------------------------------------
# Update Student City
# ----------------------------------------------------------

# SQL query to update student city
update_student = """
UPDATE students
SET city = ?
WHERE student_name = ?;
"""

# Store updated values
updated_values = (
    "Bengaluru",
    "Rohan Das"
)

# Execute update query
execute_query(conn, update_student, updated_values)

print("Student city updated successfully.")


# ----------------------------------------------------------
# Display Updated Student Record
# ----------------------------------------------------------

print("\n========== Updated Student Record ==========\n")

display_updated_student = """
SELECT *
FROM students
WHERE student_name = 'Rohan Das';
"""

print(read_query(conn, display_updated_student))


# ==========================================================
# Task 8: DELETE Operation Using Python
# ==========================================================

# ----------------------------------------------------------
# Delete Student Record
# ----------------------------------------------------------

# SQL query to delete student
delete_student = """
DELETE FROM students
WHERE student_name = ?;
"""

# Student name to delete
student_name = ("Rohan Das",)

# Execute delete query
execute_query(conn, delete_student, student_name)

print("Student record deleted successfully.")


# ----------------------------------------------------------
# Display Students Table After Deletion
# ----------------------------------------------------------

print("\n========== Students Table After Deletion ==========\n")

display_students = """
SELECT *
FROM students;
"""

print(read_query(conn, display_students))


# ==========================================================
# Task 9: Constraint Testing
# ==========================================================

# ----------------------------------------------------------
# Test 1: UNIQUE Constraint
# ----------------------------------------------------------

print("\n========== Test 1: UNIQUE Constraint ==========\n")

try:

    duplicate_student = """
    INSERT INTO students
    (student_id, student_name, email, city, registration_date)
    VALUES
    (?, ?, ?, ?, ?);
    """

    execute_query(
        conn,
        duplicate_student,
        (
            7,
            "Test Student",
            "rahul.kumar@example.com",
            "Chennai",
            "2026-02-20"
        )
    )

except sqlite3.IntegrityError as error:

    print("UNIQUE Constraint Working Successfully")
    print(error)


# ----------------------------------------------------------
# Test 2: FOREIGN KEY Constraint
# ----------------------------------------------------------

print("\n========== Test 2: FOREIGN KEY Constraint ==========\n")

try:

    invalid_enrollment = """
    INSERT INTO enrollments
    (enrollment_id, student_id, course_id, enrollment_date, status)
    VALUES
    (?, ?, ?, ?, ?);
    """

    execute_query(
        conn,
        invalid_enrollment,
        (
            2001,
            100,
            101,
            "2026-02-20",
            "Active"
        )
    )

except sqlite3.IntegrityError as error:

    print("FOREIGN KEY Constraint Working Successfully")
    print(error)


# ----------------------------------------------------------
# Test 3: CHECK Constraint
# ----------------------------------------------------------

print("\n========== Test 3: CHECK Constraint ==========\n")

try:

    invalid_course = """
    INSERT INTO courses
    (course_id, course_name, department_id, instructor_id, fee, level)
    VALUES
    (?, ?, ?, ?, ?, ?);
    """

    execute_query(
        conn,
        invalid_course,
        (
            106,
            "Cloud Computing",
            1,
            1,
            -500,
            "Beginner"
        )
    )

except sqlite3.IntegrityError as error:

    print("CHECK Constraint Working Successfully")
    print(error)


# ----------------------------------------------------------
# Test 4: CHECK Constraint On Status
# ----------------------------------------------------------

print("\n========== Test 4: CHECK Constraint On Status ==========\n")

try:

    invalid_status = """
    INSERT INTO enrollments
    (enrollment_id, student_id, course_id, enrollment_date, status)
    VALUES
    (?, ?, ?, ?, ?);
    """

    execute_query(
        conn,
        invalid_status,
        (
            2002,
            1,
            101,
            "2026-02-20",
            "Started"
        )
    )

except sqlite3.IntegrityError as error:

    print("Status CHECK Constraint Working Successfully")
    print(error)


    # ==========================================================
# Task 10: Schema Inspection
# ==========================================================

# ----------------------------------------------------------
# Inspect Students Table Structure
# ----------------------------------------------------------

print("\n========== Students Table Structure ==========\n")

students_schema = """
PRAGMA table_info(students);
"""

print(read_query(conn, students_schema))


# ----------------------------------------------------------
# Inspect Courses Table Structure
# ----------------------------------------------------------

print("\n========== Courses Table Structure ==========\n")

courses_schema = """
PRAGMA table_info(courses);
"""

print(read_query(conn, courses_schema))


# ----------------------------------------------------------
# Inspect Enrollments Table Structure
# ----------------------------------------------------------

print("\n========== Enrollments Table Structure ==========\n")

enrollments_schema = """
PRAGMA table_info(enrollments);
"""

print(read_query(conn, enrollments_schema))


# ----------------------------------------------------------
# Inspect Payments Table Structure
# ----------------------------------------------------------

print("\n========== Payments Table Structure ==========\n")

payments_schema = """
PRAGMA table_info(payments);
"""

print(read_query(conn, payments_schema))


# ----------------------------------------------------------
# Inspect Foreign Keys in Instructors Table
# ----------------------------------------------------------

print("\n========== Instructors Foreign Keys ==========\n")

instructors_fk = """
PRAGMA foreign_key_list(instructors);
"""

print(read_query(conn, instructors_fk))


# ----------------------------------------------------------
# Inspect Foreign Keys in Courses Table
# ----------------------------------------------------------

print("\n========== Courses Foreign Keys ==========\n")

courses_fk = """
PRAGMA foreign_key_list(courses);
"""

print(read_query(conn, courses_fk))


# ----------------------------------------------------------
# Inspect Foreign Keys in Enrollments Table
# ----------------------------------------------------------

print("\n========== Enrollments Foreign Keys ==========\n")

enrollments_fk = """
PRAGMA foreign_key_list(enrollments);
"""

print(read_query(conn, enrollments_fk))


# ----------------------------------------------------------
# Inspect Foreign Keys in Payments Table
# ----------------------------------------------------------

print("\n========== Payments Foreign Keys ==========\n")

payments_fk = """
PRAGMA foreign_key_list(payments);
"""

print(read_query(conn, payments_fk))


# ==========================================================
# Bonus Task: Create Course Feedback Table
# ==========================================================

# ----------------------------------------------------------
# Create Course Feedback Table
# ----------------------------------------------------------

create_feedback_table = """
CREATE TABLE IF NOT EXISTS course_feedback(

    feedback_id INTEGER PRIMARY KEY,

    enrollment_id INTEGER,

    rating INTEGER CHECK(rating BETWEEN 1 AND 5),

    comments TEXT,

    feedback_date DATE NOT NULL,

    FOREIGN KEY(enrollment_id)
    REFERENCES enrollments(enrollment_id)

);
"""

execute_query(conn, create_feedback_table)

print("Course Feedback table created successfully.")


# ----------------------------------------------------------
# Insert Feedback Records
# ----------------------------------------------------------

insert_feedback = """
INSERT OR IGNORE INTO course_feedback
(feedback_id, enrollment_id, rating, comments, feedback_date)
VALUES
(?, ?, ?, ?, ?);
"""

execute_query(
    conn,
    insert_feedback,
    (1, 1001, 5, "Excellent Course", "2026-02-10")
)

execute_query(
    conn,
    insert_feedback,
    (2, 1002, 4, "Very Good", "2026-02-11")
)

execute_query(
    conn,
    insert_feedback,
    (3, 1003, 3, "Good", "2026-02-12")
)

print("Feedback records inserted successfully.")


# ----------------------------------------------------------
# Display All Feedback
# ----------------------------------------------------------

print("\n========== All Feedback ==========\n")

all_feedback = """
SELECT *
FROM course_feedback;
"""

print(read_query(conn, all_feedback))


# ----------------------------------------------------------
# Display Feedback With Rating >= 4
# ----------------------------------------------------------

print("\n========== Feedback Rating >= 4 ==========\n")

high_rating_feedback = """
SELECT *
FROM course_feedback
WHERE rating >= 4;
"""

print(read_query(conn, high_rating_feedback))


# ----------------------------------------------------------
# Test Rating Constraint
# ----------------------------------------------------------

print("\n========== Rating Constraint Test ==========\n")

try:

    execute_query(
        conn,
        insert_feedback,
        (
            4,
            1004,
            6,
            "Invalid Rating",
            "2026-02-13"
        )
    )

except sqlite3.IntegrityError as error:

    print("Rating CHECK Constraint Working Successfully")
    print(error)

    # ==========================================================
# Close Database Connection
# ==========================================================

conn.close()

print("\nDatabase connection closed successfully.")