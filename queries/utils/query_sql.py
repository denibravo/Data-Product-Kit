import psycopg
import os
import json
import logging

# Error classes
class DatabaseConnectionError(Exception):
    pass

class DataRetrievalError(Exception):
    pass



def get_db_connection():
    '''
    Establish connection to the PostgreSQL database
    '''

    try:
        conn = psycopg.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        logging.info("Database connection successful.")
        return conn

    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise DatabaseConnectionError("Database connection failed")


def append_docket_fields(dockets_list, db_conn=None):
    '''
    Append additional fields from dockets table using docket ids from OpenSearch query results
    '''
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Use provided db_conn or create one for normal operation
    conn = db_conn if db_conn else get_db_connection()
    cursor = conn.cursor()

    try:
        # Extract docket IDs from dockets list
        docket_ids = [item["id"].strip() for item in dockets_list]
        logging.info(f"[DEBUG] Docket IDs from OpenSearch: {docket_ids}")

        # Query to fetch docket fields
        query = """
        SELECT docket_id, docket_title, modify_date, docket_type, docket_abstract
        FROM dockets 
        WHERE docket_id = ANY(%s)
        """

        cursor.execute(query, (docket_ids,))
        results = cursor.fetchall()
        docket_titles = {row[0]: row[1] for row in results}
        modify_dates = {row[0]: row[2].isoformat() for row in results}
        docket_types = {row[0]: row[3] for row in results}
        docket_abstracts = {row[0]: row[4] for row in results}

        # Append additional fields to the dockets list
        for item in dockets_list:
            item["title"] = docket_titles.get(item["id"], "Title Not Found")
            item["dateModified"] = modify_dates.get(item["id"], "Date Not Found")
            item["docketType"] = docket_types.get(item["id"], "Docket Type Not Found")
            item["summary"] = docket_abstracts.get(item["id"], "Docket Summary Not Found")

        dockets_list = [item for item in dockets_list if item["title"] != "Title Not Found"]

        logging.info("Successfully appended additional fields.")

    except Exception as e:
        logging.error(f"Error executing SQL query: {e}")
        raise DataRetrievalError("Failed to retrieve additional fields.")

    finally:
        cursor.close()
        if not db_conn:
            conn.close()
        logging.info("Database connection closed.")

    # Return the updated list
    return dockets_list


def append_agency_fields(dockets_list, db_conn=None):
    '''
    Append agency fields using docket ids from OpenSearch query results
    '''
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Use provided db_conn or create one for normal operation
    conn = db_conn if db_conn else get_db_connection()
    cursor = conn.cursor()

    try:
        # Extract docket IDs from dockets list
        docket_ids = [item["id"] for item in dockets_list]

        # Query to fetch agency fields
        query = """
        SELECT d.docket_id, a.agency_id, a.agency_name
        FROM dockets d 
        JOIN agencies a 
        ON d.agency_id = a.agency_id 
        WHERE d.docket_id = ANY(%s)
        """

        cursor.execute(query, (docket_ids,))

        # Fetch results and format them as JSON
        results = cursor.fetchall()
        agency_ids = {row[0]: row[1] for row in results}
        agency_names = {row[0]: row[2] for row in results}

        # Append agency fields to the dockets list
        for item in dockets_list:
            item["agencyID"] = agency_ids.get(item["id"], "Agency Not Found")
            item["agencyName"] = agency_names.get(item["id"], "Agency Name Not Found")

        logging.info("Successfully appended agency fields.")

    except Exception as e:
        logging.error(f"Error executing SQL query: {e}")
        raise DataRetrievalError("Failed to retrieve agency fields.")

    finally:
        cursor.close()
        if not db_conn:
            conn.close()
        logging.info("Database connection closed.")

    # Return the updated list
    return dockets_list


def append_document_counts(dockets_list, db_conn=None):
    '''
    Appends total document count and comment status from documents table to each docket in the dockets list.
    Any docket not found in the query results will default to:
      - documentCount = 0
      - isOpenForComment = False
    '''
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    conn = db_conn if db_conn else get_db_connection()
    cursor = conn.cursor()

    try:
        docket_ids = [item["id"] for item in dockets_list]

        # BOOL_OR returns True if any value is True for is_open_for_comment
        query = """
        SELECT docket_id,
               COUNT(document_id) AS document_count,
               BOOL_OR(is_open_for_comment) AS is_open
        FROM documents  
        WHERE docket_id = ANY(%s)
        GROUP BY docket_id
        """

        cursor.execute(query, (docket_ids,))
        results = cursor.fetchall()

        # Lookup dict by docket_id
        document_info = {
            row[0]: {
                "total": row[1],
                "is_open": row[2]
            }
            for row in results
        }

        # Append document counts and isOpenForComment status to dockets list
        for item in dockets_list:
            info = document_info.get(item["id"], {"total": 0, "is_open": False})
            item["documentCount"] = info["total"]
            item["isOpenForComment"] = info["is_open"]

        logging.info("Successfully appended document counts and comment status to dockets.")

    except Exception as e:
        logging.error(f"Error executing SQL query: {e}")
        raise DataRetrievalError("Failed to retrieve document counts.")

    finally:
        cursor.close()
        if not db_conn:
            conn.close()
        logging.info("Database connection closed.")

    # Return the updated list
    return dockets_list