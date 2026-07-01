import sqlite3

# Connect to database
conn = sqlite3.connect("rdbms_notebook_02.db")
cursor = conn.cursor()

# Create View
cursor.execute("""
CREATE VIEW IF NOT EXISTS vw_student_payment_summary AS
SELECT
    s.student_id,
    s.student_name,
    s.city,

    COUNT(e.enrollment_id) AS total_enrollments,

    COALESCE(SUM(
        CASE
            WHEN p.payment_status='Paid'
            THEN p.amount
            ELSE 0
        END
    ),0) AS total_paid_amount,

    COALESCE(SUM(
        CASE
            WHEN p.payment_status='Pending'
            THEN p.amount
            ELSE 0
        END
    ),0) AS total_pending_amount,

    CASE
        WHEN COALESCE(SUM(
            CASE
                WHEN p.payment_status='Paid'
                THEN p.amount
                ELSE 0
            END
        ),0) >= 20000
        THEN 'Premium Student'

        WHEN COALESCE(SUM(
            CASE
                WHEN p.payment_status='Paid'
                THEN p.amount
                ELSE 0
            END
        ),0) >= 10000
        THEN 'Regular Student'

        ELSE 'Basic Student'
    END AS student_category

FROM students s

LEFT JOIN enrollments e
ON s.student_id = e.student_id

LEFT JOIN courses c
ON e.course_id = c.course_id

LEFT JOIN payments p
ON e.enrollment_id = p.enrollment_id

GROUP BY
s.student_id,
s.student_name,
s.city;
""")

conn.commit()

# Display the View
cursor.execute("SELECT * FROM vw_student_payment_summary")

rows = cursor.fetchall()

print("\nStudent Payment Summary\n")

print("{:<10} {:<20} {:<15} {:<18} {:<18} {:<20} {:<20}".format(
    "ID",
    "Student Name",
    "City",
    "Enrollments",
    "Paid Amount",
    "Pending Amount",
    "Category"
))

print("-" * 130)

for row in rows:
    print("{:<10} {:<20} {:<15} {:<18} {:<18} {:<20} {:<20}".format(*row))

conn.close()