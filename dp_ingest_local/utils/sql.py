import os
import psycopg
from dotenv import load_dotenv

def connect():
    load_dotenv() 

    conn_params = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"), 
        "port": os.getenv("POSTGRES_PORT"),
    }

    print(f"[DEBUG] Connecting to PostgreSQL @ {conn_params['host']}:{conn_params['port']}")
    return psycopg.connect(**conn_params)
