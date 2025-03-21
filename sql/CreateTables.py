import psycopg
import sys
import os
from dotenv import load_dotenv


def _create_table(conn: psycopg.Connection, query: str, table_name: str):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            print(f"Table '{table_name}' created successfully")
    except psycopg.Error as e:
        print(f"An error occurred: {e}")


def _insert_into_table(conn: psycopg.Connection, query: str, table_name: str):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            print(f"Inserted data into '{table_name}' successfully")
    except psycopg.Error as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def create_comments_table(conn: psycopg.Connection):
    query = """
                CREATE TABLE comments (
                    comment_id VARCHAR(50) NOT NULL PRIMARY KEY,
                    api_link VARCHAR(2000) NOT NULL UNIQUE,
                    document_id VARCHAR(50) REFERENCES documents(document_id),
                    duplicate_comment_count INT DEFAULT 0 NOT NULL,
                    address1 VARCHAR(200),
                    address2 VARCHAR(200),
                    agency_id VARCHAR(20) NOT NULL,
                    city VARCHAR(100),
                    comment_category VARCHAR(200),
                    comment TEXT,
                    country VARCHAR(100),
                    docket_id VARCHAR(50) REFERENCES dockets(docket_id),
                    document_type VARCHAR(100) NOT NULL,
                    email VARCHAR(320),
                    fax VARCHAR(20),
                    flex_field1 TEXT,
                    flex_field2 TEXT,
                    first_name VARCHAR(100),
                    submitter_gov_agency VARCHAR(300),
                    submitter_gov_agency_type VARCHAR(50),
                    last_name VARCHAR(100),
                    modification_date TIMESTAMP WITH TIME ZONE,
                    submitter_org VARCHAR(200),
                    phone VARCHAR(20),
                    posted_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    postmark_date TIMESTAMP WITH TIME ZONE,
                    reason_withdrawn VARCHAR(1000),
                    received_date TIMESTAMP WITH TIME ZONE,
                    restriction_reason VARCHAR(1000),
                    restriction_reason_type VARCHAR(20),
                    state_province_region VARCHAR(100),
                    comment_subtype VARCHAR(100),
                    comment_title VARCHAR(500),
                    is_withdrawn BOOLEAN DEFAULT FALSE,
                    postal_code VARCHAR(20)
                );
            """
    _create_table(conn, query, "comments")


def create_dockets_table(conn: psycopg.Connection):
    query = """
                CREATE TABLE dockets (
                    docket_id VARCHAR(50) NOT NULL PRIMARY KEY,
                    docket_api_link VARCHAR(2000) NOT NULL UNIQUE,
                    agency_id VARCHAR(20) NOT NULL,
                    docket_category VARCHAR(100),
                    docket_type VARCHAR(50) NOT NULL,
                    effective_date TIMESTAMP WITH TIME ZONE,
                    flex_field1 TEXT,
                    flex_field2 TEXT,
                    modify_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    organization VARCHAR,
                    petition_nbr VARCHAR,
                    program VARCHAR,
                    rin VARCHAR(20),
                    short_title VARCHAR,
                    flex_subtype1 TEXT,
                    flex_subtype2 TEXT,
                    docket_title VARCHAR(500)
                );
            """
    _create_table(conn, query, "dockets")


def create_documents_table(conn: psycopg.Connection):
    query = """
                CREATE TABLE documents (
                    document_id VARCHAR(50) NOT NULL PRIMARY KEY,
                    document_api_link VARCHAR(2000) NOT NULL UNIQUE,
                    address1 VARCHAR(200),
                    address2 VARCHAR(200),
                    agency_id VARCHAR(20) NOT NULL,
                    is_late_comment BOOLEAN,
                    author_date TIMESTAMP WITH TIME ZONE,
                    comment_category VARCHAR(200),
                    city VARCHAR(100),
                    comment TEXT,
                    comment_end_date TIMESTAMP WITH TIME ZONE,
                    comment_start_date TIMESTAMP WITH TIME ZONE,
                    country VARCHAR(100),
                    docket_id VARCHAR(50) NOT NULL REFERENCES dockets(docket_id),
                    document_type CHAR(30) NOT NULL,
                    effective_date TIMESTAMP WITH TIME ZONE,
                    email VARCHAR(320),
                    fax VARCHAR(20),
                    flex_field1 TEXT,
                    flex_field2 TEXT,
                    first_name VARCHAR(100),
                    submitter_gov_agency VARCHAR(300),
                    submitter_gov_agency_type VARCHAR(50),
                    implementation_date TIMESTAMP WITH TIME ZONE,
                    last_name VARCHAR(100),
                    modify_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    is_open_for_comment BOOLEAN DEFAULT FALSE,
                    submitter_org VARCHAR(200),
                    phone VARCHAR(20),
                    posted_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    postmark_date TIMESTAMP WITH TIME ZONE,
                    reason_withdrawn VARCHAR(1000),
                    receive_date TIMESTAMP WITH TIME ZONE,
                    reg_writer_instruction TEXT,
                    restriction_reason VARCHAR(1000),
                    restriction_reason_type VARCHAR(20),
                    state_province_region VARCHAR(100),
                    subtype VARCHAR(100),
                    document_title VARCHAR(500),
                    topics VARCHAR(250)[],
                    is_withdrawn BOOLEAN DEFAULT FALSE,
                    postal_code VARCHAR(10)
                );  
            """
    _create_table(conn, query, "documents")


def create_agencies_table(conn: psycopg.Connection):
    query = """
    CREATE TABLE agencies (
        agency_id VARCHAR(20) NOT NULL PRIMARY KEY,
        agency_name VARCHAR(200) NOT NULL
    );
    """
    _create_table(conn, query, "agencies")

#def insert_agencies_data(conn: psycopg.Connection):
#    query = """
#                INSERT INTO agencies (agency_id, agency_name)
#                VALUES
#                    ('EPA', 'Environmental Protection Agency'),
#                    ('FDA', 'Food and Drug Administration
#            """
#    _insert_into_table(conn, query, "agencies")

def insert_agencies_data(conn: psycopg.Connection, file_path: str):
    try:
        with open(file_path, 'r') as file:
            # Skip the header line
            next(file)

            # Read and parse the file
            values = []
            for line in file:
                agency_id, agency_name = line.strip().split('|')
                # Escape single quotes in agency_name
                agency_name = agency_name.replace("'", "''")
                values.append(f"('{agency_id}', '{agency_name}')")

            # Construct the INSERT query
            query = f"""
            INSERT INTO agencies (agency_id, agency_name)
            VALUES {', '.join(values)};
            """

            # Execute the query
            _insert_into_table(conn, query, "agencies")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

# def insert_agencies_data(conn: psycopg.Connection, file_path: str):
#     try:
#         with open(file_path, 'r') as file:
#             # Skip the header line
#             next(file)

#             # Read and parse the file
#             values = []
#             for line in file:
#                 # Strip whitespace and skip blank or malformed lines
#                 line = line.strip()
#                 if not line or '|' not in line:
#                     continue

#                 # Split the line into agency_id and agency_name
#                 parts = line.split('|')
#                 if len(parts) != 2:
#                     print(f"Skipping malformed line: {line}")
#                     continue

#                 agency_id, agency_name = parts

#                 # Escape single quotes in agency_name
#                 agency_name = agency_name.replace("'", "''")
#                 values.append(f"('{agency_id}', '{agency_name}')")

#             # Construct the INSERT query
#             if values:  # Only execute if there are valid values
#                 query = f"""
#                 INSERT INTO agencies (agency_id, agency_name)
#                 VALUES {', '.join(values)};
#                 """
#                 # Execute the query
#                 _insert_into_table(conn, query, "agencies")
#             else:
#                 print("No valid data to insert into the agencies table.")
#     except Exception as e:
#         print(f"An error occurred while inserting data: {e}")

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
    create_dockets_table(conn)
    create_documents_table(conn)
    create_comments_table(conn)
    create_agencies_table(conn)

    # Insert data into the agencies table
    insert_agencies_data(conn, "agencies.txt")

    conn.close()


if __name__ == "__main__":
    main()
