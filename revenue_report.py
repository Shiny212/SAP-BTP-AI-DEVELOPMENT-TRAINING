import sqlite3

# Connect to the existing database
conn = sqlite3.connect("rdbms_notebook_02.db")
cursor = conn.cursor()

query = """
SELECT
    c.course_name,
    COUNT(e.enrollment_id) AS total_enrollments,
    SUM(CASE
            WHEN p.payment_status = 'Paid' THEN p.amount
            ELSE 0
        END) AS paid_revenue,
    SUM(CASE
            WHEN p.payment_status = 'Pending' THEN p.amount
            ELSE 0
        END) AS pending_amount
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
LEFT JOIN payments p
    ON e.enrollment_id = p.enrollment_id
GROUP BY c.course_id, c.course_name
ORDER BY paid_revenue DESC;
"""

cursor.execute(query)
rows = cursor.fetchall()

print("\nRevenue by Course Report\n")

print("{:<35} {:<20} {:<15} {:<15}".format(
    "Course Name",
    "Enrollments",
    "Paid Revenue",
    "Pending Amount"
))

print("-" * 90)

for row in rows:
    print("{:<35} {:<20} {:<15.1f} {:<15.1f}".format(
        row[0],
        row[1],
        row[2],
        row[3]
    ))

conn.close()