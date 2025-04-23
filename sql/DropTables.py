import psycopg
import sys
import os
from dotenv import load_dotenv


def _drop_table(conn: psycopg.Connection, table_name: str):
    try:
        with conn.cursor() as cur:
            # Check if the table exists using information_schema.tables
            cur.execute(
                """
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """,
                (table_name,),
            )
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Table '{table_name}' does not exist.")
                return

            # Drop the table if it exists
            cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
            conn.commit()
            print(f"Table '{table_name}' dropped successfully")
    except psycopg.Error as e:
        print(f"An error occurred while dropping table '{table_name}': {e}")


def drop_comments_table(conn: psycopg.Connection):
    _drop_table(conn, "comments")


def drop_dockets_table(conn: psycopg.Connection):
    _drop_table(conn, "dockets")


def drop_documents_table(conn: psycopg.Connection):
    _drop_table(conn, "documents")

def drop_stored_results_table(conn: psycopg.Connection):
    _drop_table(conn, "stored_results")


def drop_agencies_table(conn: psycopg.Connection):
    _drop_table(conn, "agencies")

def drop_abstracts_table(conn: psycopg.Connection):
    _drop_table(conn, "abstracts")

def drop_htm_summaries_table(conn: psycopg.Connection):
    _drop_table(conn, "htm_summaries")

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

    drop_comments_table(conn)
    drop_dockets_table(conn)
    drop_documents_table(conn)
    drop_agencies_table(conn)
    drop_abstracts_table(conn)
    drop_htm_summaries_table(conn)

    conn.close()


if __name__ == "__main__":
    main()
