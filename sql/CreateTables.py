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
                    phone VARCHAR(40),
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
                    docket_title VARCHAR(500),
                    docket_abstract TEXT
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
                    phone VARCHAR(40),
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

def create_stored_results_table(conn: psycopg.Connection):
    query = """
                CREATE TABLE stored_results (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(), -- when the search is initially made, so we can periodically delete old searches
                    -- info about the search: if all of these match, we return corresponding dockets
                    search_term TEXT NOT NULL,
                    session_id VARCHAR(255) NOT NULL,
                    sort_asc BOOLEAN NOT NULL,
                    sort_type VARCHAR(20) NOT NULL,
                    filter_agencies TEXT NOT NULL, -- comma separated, alphabetical order, empty string for no filter
                    filter_date_start TIMESTAMP WITH TIME ZONE NOT NULL,
                    filter_date_end TIMESTAMP WITH TIME ZONE NOT NULL,
                    filter_rulemaking VARCHAR(15) NOT NULL, -- empty string for no filter
                    -- info about the docket
                    search_rank INT NOT NULL,
                    docket_id VARCHAR(50) NOT NULL,
                    total_comments INT NOT NULL,
                    matching_comments INT NOT NULL,
                    relevance_score FLOAT NOT NULL
                );
            """
    _create_table(conn, query, "stored_results")


def create_agencies_table(conn: psycopg.Connection):
    query = """
    CREATE TABLE agencies (
        agency_id VARCHAR(20) NOT NULL PRIMARY KEY,
        agency_name VARCHAR(200) NOT NULL
    );
    """
    _create_table(conn, query, "agencies")


def create_abstracts_table(conn: psycopg.Connection):
    query = """ 
    CREATE TABLE abstracts (
        docket_id VARCHAR(50) NOT NULL REFERENCES dockets(docket_id),
        abstract TEXT
    );
    """
    _create_table(conn, query, "abstracts")


def create_htm_summaries_table(conn: psycopg.Connection):
    # other fields can be added to this to support additional fields like AI Summary
    query = """ 
    CREATE TABLE htm_summaries (
        summary_id SERIAL PRIMARY KEY,
        docket_id VARCHAR(50) NOT NULL REFERENCES dockets(docket_id),
        summary TEXT
    );
    """
    _create_table(conn, query, "htm_summaries")


def insert_agencies_data(conn: psycopg.Connection, file_path: str):
    '''
    Insert data into the agencies table from a text file called 'agencies.txt'
    The first line outlines the format of the data in the file:
    agency_id|agency_name
    '''
    try:
        with open(file_path, 'r') as file:
            # Read and parse the file
            values = []
            for line in file:
                # Skip lines starting with '#'
                if line.startswith('#'):
                    continue

                # Split the line into agency_id and agency_name
                agency_id, agency_name = line.strip().split('|')
                
                # Escape single quotes in agency_name
                agency_name = agency_name.replace("'", "''")
                values.append(f"('{agency_id}', '{agency_name}')")

            # Create the INSERT query
            query = f"""
            INSERT INTO agencies (agency_id, agency_name)
            VALUES {', '.join(values)};
            """

            # Execute the query
            _insert_into_table(conn, query, "agencies")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")


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
    create_stored_results_table(conn)
    create_htm_summaries_table(conn)
    create_abstracts_table(conn)

    # Insert data into the agencies table
    insert_agencies_data(conn, "agencies.txt")

    conn.close()


if __name__ == "__main__":
    main()
