from config import get_connection, get_schema


def run_queries():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SET SCHEMA {get_schema()}")

    print("\nCompleted Appointments\n")

    cursor.execute("""
    SELECT
        APPOINTMENT_ID,
        PATIENT_NAME,
        DOCTOR_NAME,
        DEPARTMENT_NAME,
        BILL_AMOUNT
    FROM V_OPD_APPOINTMENT_ANALYTICS
    WHERE APPOINTMENT_STATUS='Completed'
    """)

    for row in cursor.fetchall():
        print(row)

    cursor.close()
    conn.close()