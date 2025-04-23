from DropTables import drop_stored_results_table
from CreateTables import create_stored_results_table
from dotenv import load_dotenv
import psycopg
import sys
import os


def main():
    load_dotenv()

    dbname = os.getenv("POSTGRES_DB")
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn_params = {
        "dbname": dbname,
        "user": username,
        "password": password,
        "host": host,
        "port": port,
    }
    try:
        conn = psycopg.connect(**conn_params)
    except psycopg.Error as e:
        print(e)
        sys.exit(1)

    print("Dropping table")
    drop_stored_results_table(conn)

    print("\nRecreating table...")
    create_stored_results_table(conn)


if __name__ == "__main__":
    main()
