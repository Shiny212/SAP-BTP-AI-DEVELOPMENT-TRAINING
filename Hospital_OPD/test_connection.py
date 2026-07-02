from config import get_connection, get_schema

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SET SCHEMA {get_schema()}")

    cursor.execute("SELECT CURRENT_USER, CURRENT_SCHEMA FROM DUMMY")

    result = cursor.fetchall()

    print("Connected Successfully!")
    print(result)

    cursor.close()
    conn.close()

except Exception as e:
    print("Connection Failed!")
    print(e)