import json
import psycopg
from dotenv import load_dotenv
import sys
import os
from datetime import datetime


# Function to insert a summary into the database
# json_data is {"docket_id": docket_id,"summary_text": summary_text}
def insert_summary(conn, data):
    docket_id = data["docket_id"]
    summary_text = data["summary_text"]

    # get the abstract from the dockets table
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT docket_abstract from dockets where docket_id = %s
            """
            cursor.execute(query, (docket_id,))
            result = cursor.fetchone()

            abstract = result[0]

            insert_query = """
            INSERT INTO summaries (docket_id, abstract, summary) VALUES (
                %s, %s, %s
            )
            """
            cursor.execute(insert_query, (docket_id, abstract, summary_text))
            print(f"Docket summary and abstract for {docket_id} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
