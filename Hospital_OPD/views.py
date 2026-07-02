from config import get_connection, get_schema


def create_opd_analytics_view():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SET SCHEMA {get_schema()}")

    try:
        cursor.execute("DROP VIEW V_OPD_APPOINTMENT_ANALYTICS")
        print("Old OPD Analytics View Dropped")
    except:
        print("Creating New OPD Analytics View")

    cursor.execute("""
    CREATE VIEW V_OPD_APPOINTMENT_ANALYTICS AS

    SELECT

        A.APPOINTMENT_ID,
        A.APPOINTMENT_DATE,
        A.APPOINTMENT_TIME,

        P.PATIENT_NAME,
        P.CITY AS PATIENT_CITY,

        D.DOCTOR_NAME,

        DP.DEPARTMENT_NAME,

        D.SPECIALIZATION,

        D.CONSULTATION_FEE,

        B.BILL_AMOUNT,
        B.PAYMENT_MODE,
        B.PAYMENT_STATUS,

        A.APPOINTMENT_STATUS

    FROM APPOINTMENTS A

    INNER JOIN PATIENTS P
        ON A.PATIENT_ID = P.PATIENT_ID

    INNER JOIN DOCTORS D
        ON A.DOCTOR_ID = D.DOCTOR_ID

    INNER JOIN DEPARTMENTS DP
        ON D.DEPARTMENT_ID = DP.DEPARTMENT_ID

    INNER JOIN BILLING B
        ON A.APPOINTMENT_ID = B.APPOINTMENT_ID

    """)

    conn.commit()

    print("V_OPD_APPOINTMENT_ANALYTICS Created Successfully!")

    cursor.close()
    conn.close()


def create_department_daily_revenue_view():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SET SCHEMA {get_schema()}")

    try:
        cursor.execute("DROP VIEW V_DEPARTMENT_DAILY_REVENUE")
        print("Old Department Revenue View Dropped")
    except:
        print("Creating New Department Revenue View")

    cursor.execute("""

    CREATE VIEW V_DEPARTMENT_DAILY_REVENUE AS

    SELECT

        A.APPOINTMENT_DATE,

        DP.DEPARTMENT_NAME,

        COUNT(A.APPOINTMENT_ID) AS TOTAL_APPOINTMENTS,

        COUNT(B.BILL_ID) AS TOTAL_PAID_BILLS,

        SUM(B.BILL_AMOUNT) AS TOTAL_REVENUE

    FROM APPOINTMENTS A

    INNER JOIN DOCTORS D
        ON A.DOCTOR_ID = D.DOCTOR_ID

    INNER JOIN DEPARTMENTS DP
        ON D.DEPARTMENT_ID = DP.DEPARTMENT_ID

    INNER JOIN BILLING B
        ON A.APPOINTMENT_ID = B.APPOINTMENT_ID

    WHERE

        A.APPOINTMENT_STATUS='Completed'

        AND

        B.PAYMENT_STATUS='Paid'

    GROUP BY

        A.APPOINTMENT_DATE,

        DP.DEPARTMENT_NAME

    """)

    conn.commit()

    print("V_DEPARTMENT_DAILY_REVENUE Created Successfully!")

    cursor.close()
    conn.close()


if __name__ == "__main__":

    create_opd_analytics_view()

    create_department_daily_revenue_view()