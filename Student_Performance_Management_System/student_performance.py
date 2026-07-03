import csv
import numpy as np
import pandas as pd
# ==========================================
# Task 1: Basic Python Operations
# ==========================================

# Student details
student_name = "Rahul"
age = 22
city = "Patna"
course = "Python"
marks = 85
attendance_percentage = 92

# Display student details
print("Student Details")
print("---------------------------")
print("Student Name :", student_name)
print("Age          :", age)
print("City         :", city)
print("Course       :", course)
print("Marks        :", marks)
print("Attendance   :", str(attendance_percentage) + "%")


# ==========================================
# Task 2: Conditional Statements
# ==========================================

print("\nTask 2: Result and Grade")
print("---------------------------")

# Determine Result
if marks >= 40:
    result = "Pass"
else:
    result = "Fail"

# Determine Grade
if marks >= 90:
    grade = "A+"
elif marks >= 75:
    grade = "A"
elif marks >= 60:
    grade = "B"
elif marks >= 40:
    grade = "C"
else:
    grade = "Fail"

# Display Result
print("Marks  :", marks)
print("Result :", result)
print("Grade  :", grade)


# ==========================================
# Task 3: Loops
# ==========================================

print("\nTask 3: Loops")
print("---------------------------")

# List of student marks
marks_list = [85, 92, 76, 88, 69, 91, 55, 78, 39, 95]

# Print all marks
print("\nMarks Obtained:")
for mark in marks_list:
    print(mark)

# Initialize variables
passed = 0
failed = 0
total_marks = 0
highest_marks = marks_list[0]
lowest_marks = marks_list[0]

# Loop through marks
for mark in marks_list:

    # Count Pass and Fail
    if mark >= 40:
        passed += 1
    else:
        failed += 1

    # Calculate Total Marks
    total_marks += mark

    # Find Highest Marks
    if mark > highest_marks:
        highest_marks = mark

    # Find Lowest Marks
    if mark < lowest_marks:
        lowest_marks = mark

# Calculate Average
average_marks = total_marks / len(marks_list)

# Display Results
print("\nLoop Results")
print("---------------------------")
print("Passed Students :", passed)
print("Failed Students :", failed)
print("Highest Marks   :", highest_marks)
print("Lowest Marks    :", lowest_marks)
print("Total Marks     :", total_marks)
print("Average Marks   :", round(average_marks, 2))



# ==========================================
# Task 4: Data Structures
# ==========================================

print("\nTask 4: Data Structures")
print("---------------------------")

# -------------------------
# List
# -------------------------
print("\nList Example")

student_names = ["Rahul", "Priya", "Aman", "Neha", "Rohan"]

print("Original List:")
print(student_names)

# Add a new student
student_names.append("Sneha")
print("\nAfter Adding Sneha:")
print(student_names)

# Remove a student
student_names.remove("Aman")
print("\nAfter Removing Aman:")
print(student_names)

# Print all students using a loop
print("\nStudent Names:")
for name in student_names:
    print(name)

# -------------------------
# Tuple
# -------------------------
print("\nTuple Example")

courses = ("Python", "Data Science", "Analytics")

print("Courses:")
for course in courses:
    print(course)

print("\nSecond Course:", courses[1])

# -------------------------
# Set
# -------------------------
print("\nSet Example")

cities = {"Patna", "Delhi", "Kolkata", "Mumbai"}

print("Unique Cities:")
print(cities)

# Add a new city
cities.add("Chennai")
print("\nAfter Adding Chennai:")
print(cities)

# Remove a city
cities.remove("Mumbai")
print("\nAfter Removing Mumbai:")
print(cities)

# -------------------------
# Dictionary
# -------------------------
print("\nDictionary Example")

student = {
    "Student_ID": 1,
    "Name": "Rahul",
    "Age": 22,
    "City": "Patna",
    "Course": "Python",
    "Marks": 85,
    "Attendance_Percentage": 92
}

# Print student name
print("Student Name:", student["Name"])

# Update marks
student["Marks"] = 90

# Add Result
student["Result"] = "Pass"

print("\nUpdated Student Dictionary")

for key, value in student.items():
    print(key, ":", value)



    # ==========================================
# Task 5: Functions
# ==========================================

print("\nTask 5: Functions")
print("---------------------------")

# Function to calculate result
def calculate_result(marks):
    if marks >= 40:
        return "Pass"
    else:
        return "Fail"


# Function to calculate grade
def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 40:
        return "C"
    else:
        return "Fail"


# Function to calculate average marks
def calculate_average(marks_list):
    return sum(marks_list) / len(marks_list)


# Function to check attendance status
def attendance_status(attendance):
    if attendance >= 75:
        return "Eligible"
    else:
        return "Low Attendance"


# Test the functions
student_marks = 85
student_attendance = 92

print("Marks:", student_marks)
print("Result:", calculate_result(student_marks))
print("Grade:", calculate_grade(student_marks))
print("Average Marks:", round(calculate_average(marks_list), 2))
print("Attendance Status:", attendance_status(student_attendance))



# ==========================================
# Task 6: Error Handling
# ==========================================

print("\nTask 6: Error Handling")
print("---------------------------")

try:
    user_marks = float(input("Enter student marks (0-100): "))

    if user_marks < 0 or user_marks > 100:
        print("Invalid input. Please enter marks between 0 and 100.")
    else:
        print("Marks Entered:", user_marks)

        if user_marks >= 40:
            print("Result: Pass")
        else:
            print("Result: Fail")

except ValueError:
    print("Invalid input. Please enter a numeric value.")



    # ==========================================
# Task 7: File Handling
# ==========================================

print("\nTask 7: File Handling")
print("---------------------------")

# Create and write to the text file
with open("student_summary.txt", "w") as file:
    file.write("Student Performance Summary\n")
    file.write("---------------------------\n")
    file.write("Total Students: 10\n")
    file.write("Average Marks: 76.8\n")
    file.write("Highest Marks: 95\n")
    file.write("Lowest Marks: 39\n")
    file.write("Passed Students: 9\n")
    file.write("Failed Students: 1\n")

print("student_summary.txt created successfully.")

# Read and display the file content
print("\nContents of student_summary.txt:\n")

with open("student_summary.txt", "r") as file:
    content = file.read()
    print(content)



    # ==========================================
# Task 8: CSV File Handling
# ==========================================

print("\nTask 8: CSV File Handling")
print("---------------------------")

# Student records
students = [
    [1, "Rahul", 22, "Patna", "Python", 85, 92],
    [2, "Priya", 24, "Delhi", "Data Science", 92, 88],
    [3, "Aman", 21, "Kolkata", "Python", 76, 81],
    [4, "Neha", 23, "Mumbai", "Analytics", 88, 95],
    [5, "Rohan", 25, "Patna", "Python", 69, 72],
    [6, "Simran", 22, "Delhi", "Data Science", 91, 89],
    [7, "Vikash", 24, "Patna", "Analytics", 55, 68],
    [8, "Pooja", 21, "Kolkata", "Python", 78, 84],
    [9, "Arjun", 23, "Mumbai", "Data Science", 39, 60],
    [10, "Sneha", 22, "Delhi", "Python", 95, 97]
]

# Write data into CSV
with open("students.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow([
        "Student_ID",
        "Name",
        "Age",
        "City",
        "Course",
        "Marks",
        "Attendance_Percentage"
    ])

    # Student Records
    writer.writerows(students)

print("students.csv created successfully.")

# Read CSV file
print("\nStudent Records:\n")

with open("students.csv", "r") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)



        # ==========================================
# Task 9: NumPy Analysis
# ==========================================

print("\nTask 9: NumPy Analysis")
print("---------------------------")

# Create NumPy array of marks
marks_array = np.array([85, 92, 76, 88, 69, 91, 55, 78, 39, 95])

# Calculations
total_marks = np.sum(marks_array)
average_marks = np.mean(marks_array)
highest_marks = np.max(marks_array)
lowest_marks = np.min(marks_array)
standard_deviation = np.std(marks_array)

# Display Results
print("Marks Array:", marks_array)
print("Total Marks:", total_marks)
print("Average Marks:", round(average_marks, 2))
print("Highest Marks:", highest_marks)
print("Lowest Marks:", lowest_marks)
print("Standard Deviation:", round(standard_deviation, 2))



# ==========================================
# Task 10: Pandas Data Analysis
# ==========================================

print("\nTask 10: Pandas Data Analysis")
print("---------------------------")

# Read the CSV file
df = pd.read_csv("students.csv")

# Display first five rows
print("\nFirst Five Rows")
print(df.head())

# Display last five rows
print("\nLast Five Rows")
print(df.tail())

# Display dataset shape
print("\nDataset Shape")
print(df.shape)

# Display column names
print("\nColumn Names")
print(df.columns)

# Display dataset information
print("\nDataset Information")
df.info()

# Display statistical summary
print("\nStatistical Summary")
print(df.describe())



# ==========================================
# Task 11: Pandas Filtering
# ==========================================

print("\nTask 11: Pandas Filtering")
print("---------------------------")

# Students who scored more than 80 marks
print("\nStudents Who Scored More Than 80 Marks")
print(df[df["Marks"] > 80])

# Students whose attendance is below 75%
print("\nStudents Whose Attendance is Below 75%")
print(df[df["Attendance_Percentage"] < 75])

# Students from Patna
print("\nStudents From Patna")
print(df[df["City"] == "Patna"])

# Students enrolled in Python course
print("\nStudents Enrolled in Python Course")
print(df[df["Course"] == "Python"])

# Students who failed
print("\nStudents Who Failed")
print(df[df["Marks"] < 40])



# ==========================================
# Task 12: Pandas Sorting
# ==========================================

print("\nTask 12: Pandas Sorting")
print("---------------------------")

# Sort by Marks (Highest to Lowest)
print("\nStudents Sorted by Marks (Descending)")
marks_sorted = df.sort_values(by="Marks", ascending=False)
print(marks_sorted)

# Sort by Attendance Percentage (Highest to Lowest)
print("\nStudents Sorted by Attendance (Descending)")
attendance_sorted = df.sort_values(by="Attendance_Percentage", ascending=False)
print(attendance_sorted)

# Sort by Name (Alphabetical Order)
print("\nStudents Sorted by Name (A-Z)")
name_sorted = df.sort_values(by="Name", ascending=True)
print(name_sorted)



# ==========================================
# Task 13: Add New Columns
# ==========================================

print("\nTask 13: Add New Columns")
print("---------------------------")

# Add Result Column
df["Result"] = df["Marks"].apply(lambda marks: "Pass" if marks >= 40 else "Fail")

# Add Grade Column
def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 40:
        return "C"
    else:
        return "Fail"

df["Grade"] = df["Marks"].apply(calculate_grade)

# Add Attendance_Status Column
df["Attendance_Status"] = df["Attendance_Percentage"].apply(
    lambda attendance: "Eligible" if attendance >= 75 else "Low Attendance"
)

# Display the updated DataFrame
print(df)



# ==========================================
# Task 14: Grouping and Aggregation
# ==========================================

print("\nTask 14: Grouping and Aggregation")
print("---------------------------")

# Count students city-wise
print("\nStudent Count City-wise")
city_count = df.groupby("City")["Student_ID"].count()
print(city_count)

# Count students course-wise
print("\nStudent Count Course-wise")
course_count = df.groupby("Course")["Student_ID"].count()
print(course_count)

# Average marks course-wise
print("\nAverage Marks Course-wise")
avg_marks = df.groupby("Course")["Marks"].mean()
print(avg_marks)

# Average attendance city-wise
print("\nAverage Attendance City-wise")
avg_attendance = df.groupby("City")["Attendance_Percentage"].mean()
print(avg_attendance)

# Highest marks in each course
print("\nHighest Marks in Each Course")
highest_marks = df.groupby("Course")["Marks"].max()
print(highest_marks)




# ==========================================
# Task 15: Final Mini Project Report
# ==========================================

print("\nTask 15: Final Mini Project Report")
print("---------------------------")

# Calculate summary metrics
total_students = len(df)
average_marks = df["Marks"].mean()
highest_marks = df["Marks"].max()
lowest_marks = df["Marks"].min()
passed_students = len(df[df["Result"] == "Pass"])
failed_students = len(df[df["Result"] == "Fail"])
low_attendance = len(df[df["Attendance_Status"] == "Low Attendance"])
students_above_80 = len(df[df["Marks"] > 80])

# Create summary report
summary = {
    "Metric": [
        "Total Students",
        "Average Marks",
        "Highest Marks",
        "Lowest Marks",
        "Passed Students",
        "Failed Students",
        "Students with Low Attendance",
        "Students Scoring Above 80"
    ],
    "Value": [
        total_students,
        round(average_marks, 2),
        highest_marks,
        lowest_marks,
        passed_students,
        failed_students,
        low_attendance,
        students_above_80
    ]
}

summary_df = pd.DataFrame(summary)

# Display summary
print(summary_df)

# Save updated dataset
df.to_csv("final_student_performance_report.csv", index=False)

print("\nfinal_student_performance_report.csv created successfully.")