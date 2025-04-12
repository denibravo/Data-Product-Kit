import json
import psycopg
from dotenv import load_dotenv
import sys
import os
from datetime import datetime

# Fetch database connection parameters from environment variables


# Function to parse date fields
def _parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return None


# Function to insert docket into the database
def insert_docket(conn, json_data):
    # Parse the JSON data
    data = json.loads(json_data)

    # Extract relevant fields
    attributes = data["data"]["attributes"]
    docket_id = data["data"]["id"]
    docket_api_link = data["data"]["links"]["self"]

    # Prepare the values for insertion
    values = (
        docket_id,
        docket_api_link,
        attributes["agencyId"],
        attributes["category"],
        attributes["docketType"],
        _parse_date(attributes["effectiveDate"]),
        attributes["field1"],
        attributes["field2"],
        _parse_date(attributes["modifyDate"]),
        attributes["organization"],
        attributes["petitionNbr"],
        attributes["program"],
        attributes["rin"],
        attributes["shortTitle"],
        attributes["subType"],
        attributes["subType2"],
        attributes["title"],
    )

    # Insert into the database
    try:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO dockets (
                docket_id, docket_api_link, agency_id, docket_category, docket_type,
                effective_date, flex_field1, flex_field2, modify_date, organization,
                petition_nbr, program, rin, short_title, flex_subtype1, flex_subtype2,
                docket_title
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, values)
            print(f"Docket {docket_id} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Main function to read JSON from file and insert into the database
def main():
    if len(sys.argv) != 2:
        print("Usage: python IngestDocket.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
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
        with open(json_file_path, "r") as json_file:
            json_data = json_file.read()
            with psycopg.connect(**conn_params) as conn:
                insert_docket(conn, json_data)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
