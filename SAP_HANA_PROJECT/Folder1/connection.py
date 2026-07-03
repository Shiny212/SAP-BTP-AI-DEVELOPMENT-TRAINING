from hdbcli import dbapi

try:
    conn = dbapi.connect(
        address="13b7c15d-848f-40b5-9259-c9c36ab85f56.hna1.prod-eu10.hanacloud.ondemand.com",
        port=443,
        user="GE336922",
        password="Obmc5sMvot1!",
        encrypt=True,
        sslValidateCertificate=False
    )

    print("Connected Successfully!")

    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_USER FROM DUMMY")

    for row in cursor.fetchall():
        print(row)

    cursor.close()
    conn.close()

except Exception as e:
    print("Connection Failed!")
    print(e)