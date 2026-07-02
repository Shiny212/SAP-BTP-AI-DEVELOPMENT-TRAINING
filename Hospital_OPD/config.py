import os
from dotenv import load_dotenv
from hdbcli import dbapi

# Load variables from .env
load_dotenv()

def get_connection():
    conn = dbapi.connect(
        address=os.getenv("HANA_HOST"),
        port=int(os.getenv("HANA_PORT")),
        user=os.getenv("HANA_USER"),
        password=os.getenv("HANA_PASSWORD"),
        encrypt=True,
        sslValidateCertificate=False
    )
    return conn


def get_schema():
    return os.getenv("HANA_SCHEMA")