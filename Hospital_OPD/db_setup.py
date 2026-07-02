from config import get_connection, get_schema

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SET SCHEMA {get_schema()}")

    # Drop tables if they already exist
    tables = ["BILLING", "APPOINTMENTS", "DOCTORS", "DEPARTMENTS", "PATIENTS"]

    for table in tables:
        try:
            cursor.execute(f"DROP TABLE {table}")
            print(f"{table} dropped")
        except Exception:
            print(f"{table} does not exist")

    # ---------------- PATIENTS ----------------
    cursor.execute("""
    CREATE COLUMN TABLE PATIENTS(
        PATIENT_ID INTEGER PRIMARY KEY,
        PATIENT_NAME NVARCHAR(100),
        GENDER NVARCHAR(10),
        AGE INTEGER,
        CITY NVARCHAR(50),
        MOBILE_NUMBER NVARCHAR(15)
    )
    """)

    print("PATIENTS Created")

    # ---------------- DEPARTMENTS ----------------
    cursor.execute("""
    CREATE COLUMN TABLE DEPARTMENTS(
        DEPARTMENT_ID INTEGER PRIMARY KEY,
        DEPARTMENT_NAME NVARCHAR(100),
        FLOOR_NUMBER INTEGER
    )
    """)

    print("DEPARTMENTS Created")

    # ---------------- DOCTORS ----------------
    cursor.execute("""
    CREATE COLUMN TABLE DOCTORS(
        DOCTOR_ID INTEGER PRIMARY KEY,
        DOCTOR_NAME NVARCHAR(100),
        DEPARTMENT_ID INTEGER,
        SPECIALIZATION NVARCHAR(100),
        CONSULTATION_FEE DECIMAL(10,2),

        FOREIGN KEY (DEPARTMENT_ID)
        REFERENCES DEPARTMENTS(DEPARTMENT_ID)
    )
    """)

    print("DOCTORS Created")

    # ---------------- APPOINTMENTS ----------------
    cursor.execute("""
    CREATE COLUMN TABLE APPOINTMENTS(
        APPOINTMENT_ID INTEGER PRIMARY KEY,
        PATIENT_ID INTEGER,
        DOCTOR_ID INTEGER,
        APPOINTMENT_DATE DATE,
        APPOINTMENT_TIME TIME,
        APPOINTMENT_STATUS NVARCHAR(20),

        FOREIGN KEY(PATIENT_ID)
        REFERENCES PATIENTS(PATIENT_ID),

        FOREIGN KEY(DOCTOR_ID)
        REFERENCES DOCTORS(DOCTOR_ID)
    )
    """)

    print("APPOINTMENTS Created")

    # ---------------- BILLING ----------------
    cursor.execute("""
    CREATE COLUMN TABLE BILLING(
        BILL_ID INTEGER PRIMARY KEY,
        APPOINTMENT_ID INTEGER,
        BILL_AMOUNT DECIMAL(10,2),
        PAYMENT_MODE NVARCHAR(20),
        PAYMENT_STATUS NVARCHAR(20),

        FOREIGN KEY(APPOINTMENT_ID)
        REFERENCES APPOINTMENTS(APPOINTMENT_ID)
    )
    """)

    print("BILLING Created")

    conn.commit()

    print("\nAll Tables Created Successfully!")

    cursor.close()
    conn.close()