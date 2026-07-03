from hdbcli import dbapi

conn = dbapi.connect(
    address="13b7c15d-848f-40b5-9259-c9c36ab85f56.hna1.prod-eu10.hanacloud.ondemand.com",
    port=443,
    user="GE336922",
    password="Obmc5sMvot1!",
    encrypt=True,
    sslValidateCertificate=False
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM CANDIDATES")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()