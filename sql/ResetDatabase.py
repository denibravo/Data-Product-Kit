from DropTables import (
    drop_comments_table,
    drop_dockets_table,
    drop_documents_table,
    drop_agencies_table,
    drop_stored_results_table,
    drop_summaries_table,
)
from CreateTables import (
    create_comments_table,
    create_dockets_table,
    create_documents_table,
    create_stored_results_table,
    create_agencies_table,
    insert_agencies_data,
    create_summaries_table,
)
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

    print("Dropping tables")
    drop_comments_table(conn)
    drop_documents_table(conn)
    drop_dockets_table(conn)
    drop_stored_results_table(conn)
    drop_agencies_table(conn)
    drop_summaries_table(conn)

    print("\nRecreating tables...")
    create_dockets_table(conn)
    create_documents_table(conn)
    create_comments_table(conn)
    create_stored_results_table(conn)
    create_agencies_table(conn)
    create_summaries_table(conn)

    print("\nInserting data into the agencies table...")
    insert_agencies_data(conn, "agencies.txt")


if __name__ == "__main__":
    main()
