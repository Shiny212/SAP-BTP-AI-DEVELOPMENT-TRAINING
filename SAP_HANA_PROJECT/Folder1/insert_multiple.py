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

data = [
    (2, "Rahul", 24),
    (3, "Priya", 21),
    (4, "Arun", 25),
    (5, "Meena", 23)
]

cursor.executemany(
    "INSERT INTO CANDIDATES VALUES (?, ?, ?)",
    data
)

conn.commit()

print("Multiple Records Inserted Successfully!")

cursor.close()
conn.close()