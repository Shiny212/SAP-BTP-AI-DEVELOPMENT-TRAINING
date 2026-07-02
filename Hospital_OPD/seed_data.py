from config import get_connection, get_schema


def insert_sample_data():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SET SCHEMA {get_schema()}")

    # ---------------- PATIENTS ----------------
    patients = [
        (1, "Rahul Kumar", "Male", 32, "Patna", "9876543210"),
        (2, "Sneha Singh", "Female", 28, "Kolkata", "9876501234"),
        (3, "Amit Sharma", "Male", 45, "Patna", "9123456789"),
        (4, "Priya Verma", "Female", 36, "Ranchi", "9988776655"),
        (5, "Rohan Gupta", "Male", 52, "Gaya", "9876123450"),
        (6, "Neha Kumari", "Female", 24, "Patna", "9123987654"),
        (7, "Vikash Raj", "Male", 40, "Muzaffarpur", "9090909090"),
        (8, "Anjali Sinha", "Female", 31, "Bhagalpur", "9000011112")
    ]

    cursor.executemany("""
        INSERT INTO PATIENTS
        VALUES (?,?,?,?,?,?)
    """, patients)

    print("✅ PATIENTS inserted")

    # ---------------- DEPARTMENTS ----------------
    departments = [
        (101, "General Medicine", 1),
        (102, "Cardiology", 2),
        (103, "Orthopedics", 3),
        (104, "Pediatrics", 1),
        (105, "Dermatology", 2)
    ]

    cursor.executemany("""
        INSERT INTO DEPARTMENTS
        VALUES (?,?,?)
    """, departments)

    print("✅ DEPARTMENTS inserted")

    # ---------------- DOCTORS ----------------
    doctors = [
        (201, "Dr. Arvind Kumar", 101, "General Physician", 500),
        (202, "Dr. Meera Singh", 102, "Cardiologist", 1000),
        (203, "Dr. Rajesh Prasad", 103, "Orthopedic Surgeon", 800),
        (204, "Dr. Pooja Verma", 104, "Child Specialist", 600),
        (205, "Dr. Kunal Sinha", 105, "Skin Specialist", 700),
        (206, "Dr. Nidhi Sharma", 101, "Internal Medicine", 650)
    ]

    cursor.executemany("""
        INSERT INTO DOCTORS
        VALUES (?,?,?,?,?)
    """, doctors)

    print("✅ DOCTORS inserted")

    # ---------------- APPOINTMENTS ----------------
    appointments = [
        (3001, 1, 201, "2026-07-01", "10:00:00", "Completed"),
        (3002, 2, 202, "2026-07-01", "11:00:00", "Completed"),
        (3003, 3, 203, "2026-07-01", "12:30:00", "Pending"),
        (3004, 4, 204, "2026-07-02", "09:30:00", "Completed"),
        (3005, 5, 202, "2026-07-02", "13:00:00", "Cancelled"),
        (3006, 6, 205, "2026-07-02", "15:00:00", "Completed"),
        (3007, 7, 206, "2026-07-03", "10:30:00", "Completed"),
        (3008, 8, 203, "2026-07-03", "11:30:00", "Pending"),
        (3009, 1, 202, "2026-07-04", "14:00:00", "Completed"),
        (3010, 3, 201, "2026-07-04", "16:00:00", "Completed")
    ]

    cursor.executemany("""
        INSERT INTO APPOINTMENTS
        VALUES (?,?,?,?,?,?)
    """, appointments)

    print("✅ APPOINTMENTS inserted")

    # ---------------- BILLING ----------------
    billing = [
        (4001, 3001, 500, "UPI", "Paid"),
        (4002, 3002, 1000, "Card", "Paid"),
        (4003, 3003, 800, "Cash", "Unpaid"),
        (4004, 3004, 600, "UPI", "Paid"),
        (4005, 3005, 1000, "Card", "Refunded"),
        (4006, 3006, 700, "Cash", "Paid"),
        (4007, 3007, 650, "UPI", "Paid"),
        (4008, 3008, 800, "Cash", "Unpaid"),
        (4009, 3009, 1000, "Insurance", "Paid"),
        (4010, 3010, 500, "UPI", "Paid")
    ]

    cursor.executemany("""
        INSERT INTO BILLING
        VALUES (?,?,?,?,?)
    """, billing)

    print("✅ BILLING inserted")

    conn.commit()

    print("\n🎉 Sample Data Inserted Successfully!")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    insert_sample_data()