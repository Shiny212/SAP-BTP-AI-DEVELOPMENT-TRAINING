import sqlite3

# Create Database
conn = sqlite3.connect("hr_management.db")

# Enable Foreign Keys
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

# ==========================
# Departments Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments(
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE
)
""")

# ==========================
# Job Roles Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS job_roles(
    role_id INTEGER PRIMARY KEY,
    role_title TEXT NOT NULL UNIQUE,
    min_salary REAL NOT NULL CHECK(min_salary>=0),
    max_salary REAL NOT NULL CHECK(max_salary>=min_salary)
)
""")

# ==========================
# Employees Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    city TEXT,
    joining_date DATE,
    department_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    status TEXT DEFAULT 'Active'
        CHECK(status IN('Active','Probation','Resigned')),

    FOREIGN KEY(department_id)
        REFERENCES departments(department_id),

    FOREIGN KEY(role_id)
        REFERENCES job_roles(role_id)
)
""")

# ==========================
# Attendance Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(

    attendance_id INTEGER PRIMARY KEY,

    employee_id INTEGER NOT NULL,

    attendance_date DATE NOT NULL,

    attendance_status TEXT NOT NULL
        CHECK(attendance_status IN
        ('Present','Absent','Leave','Half Day')),

    FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id),

    UNIQUE(employee_id,attendance_date)
)
""")

# ==========================
# Payroll Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS payroll(

    payroll_id INTEGER PRIMARY KEY,

    employee_id INTEGER NOT NULL,

    salary_month TEXT NOT NULL,

    basic_salary REAL NOT NULL
        CHECK(basic_salary>=0),

    bonus REAL DEFAULT 0
        CHECK(bonus>=0),

    deductions REAL DEFAULT 0
        CHECK(deductions>=0),

    payment_status TEXT
        CHECK(payment_status IN
        ('Paid','Pending','Hold')),

    FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id),

    UNIQUE(employee_id,salary_month)
)
""")
# ==========================
# Insert Departments
# ==========================

cursor.executemany("""
INSERT OR IGNORE INTO departments
VALUES (?,?)
""",[
(1,"Human Resources"),
(2,"Information Technology"),
(3,"Finance"),
(4,"Sales"),
(5,"Operations")
])

# ==========================
# Insert Job Roles
# ==========================

cursor.executemany("""
INSERT OR IGNORE INTO job_roles
VALUES (?,?,?,?)
""",[
(1,"HR Executive",25000,50000),
(2,"Software Developer",40000,100000),
(3,"Accountant",30000,70000),
(4,"Sales Executive",25000,60000),
(5,"Operations Associate",25000,55000)
])

# ==========================
# Insert Employees
# ==========================

cursor.executemany("""
INSERT OR IGNORE INTO employees
VALUES (?,?,?,?,?,?,?,?)
""",[
(1,"Rahul Kumar","rahul@example.com","Patna","2026-01-10",2,2,"Active"),
(2,"Priya Singh","priya@example.com","Kolkata","2026-01-12",3,3,"Active"),
(3,"Amit Raj","amit@example.com","Delhi","2026-01-15",2,2,"Probation"),
(4,"Sneha Verma","sneha@example.com","Patna","2026-01-18",1,1,"Active"),
(5,"Aditya Sharma","aditya@example.com","Mumbai","2026-01-20",5,5,"Active")
])

# ==========================
# Insert Attendance
# ==========================

cursor.executemany("""
INSERT OR IGNORE INTO attendance
VALUES (?,?,?,?)
""",[
(1,1,"2026-02-01","Present"),
(2,2,"2026-02-01","Present"),
(3,3,"2026-02-01","Leave"),
(4,4,"2026-02-01","Half Day"),
(5,5,"2026-02-01","Absent")
])

# ==========================
# Insert Payroll
# ==========================

cursor.executemany("""
INSERT OR IGNORE INTO payroll
VALUES (?,?,?,?,?,?,?)
""",[
(1,1,"2026-02",35000,2000,1000,"Paid"),
(2,2,"2026-02",80000,5000,2000,"Paid"),
(3,3,"2026-02",45000,0,1000,"Pending"),
(4,4,"2026-02",30000,3000,500,"Paid"),
(5,5,"2026-02",28000,0,0,"Hold")
])

conn.commit()


print("Database Created Successfully")
print("All 5 Tables Created Successfully")
print("\nSample Data Inserted Successfully")
print("\n========== Departments ==========")

cursor.execute("SELECT * FROM departments")

for row in cursor.fetchall():
    print(row)
print("\n========== Job Roles ==========")

cursor.execute("SELECT * FROM job_roles")

for row in cursor.fetchall():
    print(row)
print("\n========== Employees ==========")

cursor.execute("SELECT * FROM employees")

for row in cursor.fetchall():
    print(row)
print("\n========== Attendance ==========")

cursor.execute("SELECT * FROM attendance")

for row in cursor.fetchall():
    print(row)
print("\n========== Payroll ==========")

cursor.execute("SELECT * FROM payroll")

for row in cursor.fetchall():
    print(row)
print("\n========== 1. All Employees ==========")

cursor.execute("SELECT * FROM employees")

for row in cursor.fetchall():
    print(row)
print("\n========== 2. Employee Name, Email and City ==========")

cursor.execute("""
SELECT employee_name,email,city
FROM employees
""")

for row in cursor.fetchall():
    print(row)
print("\n========== 3. Employees from Patna ==========")

cursor.execute("""
SELECT *
FROM employees
WHERE city='Patna'
""")

for row in cursor.fetchall():
    print(row)
print("\n========== 4. Active Employees ==========")

cursor.execute("""
SELECT *
FROM employees
WHERE status='Active'
""")

for row in cursor.fetchall():
    print(row)
print("\n========== 5. Employees under Probation ==========")

cursor.execute("""
SELECT *
FROM employees
WHERE status='Probation'
""")

for row in cursor.fetchall():
    print(row)
print("\n========== 6. Employees by Joining Date ==========")

cursor.execute("""
SELECT *
FROM employees
ORDER BY joining_date
""")

for row in cursor.fetchall():
    print(row)
print("\n========== 7. Top 3 Highest Paid Employees ==========")

cursor.execute("""
SELECT
e.employee_name,
p.basic_salary
FROM employees e
JOIN payroll p
ON e.employee_id=p.employee_id
ORDER BY p.basic_salary DESC
LIMIT 3
""")

for row in cursor.fetchall():
    print(row)
print("\n========== 8. Distinct Cities ==========")

cursor.execute("""
SELECT DISTINCT city
FROM employees
""")

for row in cursor.fetchall():
    print(row)
print("\n========== 9. Pending Payroll ==========")

cursor.execute("""
SELECT *
FROM payroll
WHERE payment_status='Pending'
""")

for row in cursor.fetchall():
    print(row)
print("\n========== 10. Absent Employees ==========")

cursor.execute("""
SELECT *
FROM attendance
WHERE attendance_status='Absent'
""")

for row in cursor.fetchall():
    print(row)
print("\n========== Task 7 : Insert New Employee ==========")

cursor.execute("""
INSERT INTO employees
(employee_id, employee_name, email, city, joining_date, department_id, role_id, status)
VALUES
(6,
'Rohan Das',
'rohan.hr@example.com',
'Pune',
'2026-02-15',
1,
1,
'Probation')
""")

conn.commit()

cursor.execute("""
SELECT *
FROM employees
WHERE employee_name='Rohan Das'
""")

for row in cursor.fetchall():
    print(row)
print("\n========== Task 8 : Update City ==========")

cursor.execute("""
UPDATE employees
SET city='Bengaluru'
WHERE employee_name='Rohan Das'
""")

conn.commit()

cursor.execute("""
SELECT *
FROM employees
WHERE employee_name='Rohan Das'
""")

for row in cursor.fetchall():
    print(row)
print("\n========== Task 9 : Update Status ==========")

cursor.execute("""
UPDATE employees
SET status='Active'
WHERE employee_name='Rohan Das'
""")

conn.commit()

cursor.execute("""
SELECT *
FROM employees
WHERE employee_name='Rohan Das'
""")

for row in cursor.fetchall():
    print(row)
print("\n========== Task 10 : Delete Employee ==========")

cursor.execute("""
DELETE FROM employees
WHERE employee_name='Rohan Das'
""")

conn.commit()

cursor.execute("""
SELECT *
FROM employees
""")

for row in cursor.fetchall():
    print(row)
print("\n========== Test 1 : Duplicate Email ==========")

try:
    cursor.execute("""
    INSERT INTO employees
    VALUES
    (7,'Test Employee','rahul@example.com','Chennai',
    '2026-03-01',1,1,'Active')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Test 2 : Invalid Department ==========")

try:
    cursor.execute("""
    INSERT INTO employees
    VALUES
    (8,'Test Employee2','test2@example.com','Chennai',
    '2026-03-01',99,1,'Active')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Test 3 : Invalid Job Role ==========")

try:
    cursor.execute("""
    INSERT INTO employees
    VALUES
    (9,'Test Employee3','test3@example.com','Delhi',
    '2026-03-01',1,99,'Active')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Test 4 : Invalid Employee Status ==========")

try:
    cursor.execute("""
    INSERT INTO employees
    VALUES
    (10,'Test Employee4','test4@example.com','Mumbai',
    '2026-03-01',1,1,'Joined')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Test 5 : Duplicate Attendance ==========")

try:
    cursor.execute("""
    INSERT INTO attendance
    VALUES
    (6,1,'2026-02-01','Present')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Test 6 : Invalid Attendance Status ==========")

try:
    cursor.execute("""
    INSERT INTO attendance
    VALUES
    (7,1,'2026-02-02','Late')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Test 7 : Duplicate Payroll ==========")

try:
    cursor.execute("""
    INSERT INTO payroll
    VALUES
    (6,1,'2026-02',35000,1000,0,'Paid')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Test 8 : Negative Salary ==========")

try:
    cursor.execute("""
    INSERT INTO payroll
    VALUES
    (7,2,'2026-03',-5000,0,0,'Paid')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Test 9 : Invalid Payroll Status ==========")

try:
    cursor.execute("""
    INSERT INTO payroll
    VALUES
    (8,2,'2026-03',50000,0,0,'Processing')
    """)
    conn.commit()
except Exception as e:
    print(e)
print("\n========== Departments Schema ==========")
cursor.execute("PRAGMA table_info(departments)")
print(cursor.fetchall())

print("\n========== Job Roles Schema ==========")
cursor.execute("PRAGMA table_info(job_roles)")
print(cursor.fetchall())

print("\n========== Employees Schema ==========")
cursor.execute("PRAGMA table_info(employees)")
print(cursor.fetchall())

print("\n========== Attendance Schema ==========")
cursor.execute("PRAGMA table_info(attendance)")
print(cursor.fetchall())

print("\n========== Payroll Schema ==========")
cursor.execute("PRAGMA table_info(payroll)")
print(cursor.fetchall())

conn.close()