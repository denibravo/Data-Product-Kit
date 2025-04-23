from .utilities.ingest_comment import insert_comment
from .utilities.ingest_docket import insert_docket
from .utilities.ingest_document import insert_document
import boto3
import sys
import os
import psycopg
from dotenv import load_dotenv


def get_agency(docket_id: str) -> str:
    return docket_id.split("-")[0]


def get_text_content_from_s3(bucket, file_key: str):
    try:
        obj = bucket.Object(file_key)
        text = obj.get()["Body"].read().decode("utf-8")

        return text
    except Exception as e:
        print(f"Error retrieving JSON file {file_key}, {e}")
        return None


def process_comments(bucket, conn, s3_path):
    text = get_text_content_from_s3(bucket, s3_path)
    insert_comment(conn, text)


def process_dockets(bucket, conn, s3_path):
    text = get_text_content_from_s3(bucket, s3_path)
    insert_docket(conn, text)


def process_documents(bucket, conn, s3_path):
    text = get_text_content_from_s3(bucket, s3_path)
    insert_document(conn, text)


def sort_files(files_list) -> list[str]:
    # Define the order of categories
    category_order = {"docket": 1, "documents": 2, "comments": 3}

    # Function to determine the sorting key
    def sorting_key(file_path):
        # Check which category the file belongs to
        for category in category_order.keys():
            if category in file_path:
                return category_order[category]
        return float("inf")  # If no category is found, place it at the end

    # Sort the files based on the defined order
    sorted_files = sorted(files_list, key=sorting_key)

    return sorted_files


def categorize_and_process_files(bucket, conn, file_list):
    exclude_keywords = [
        "binary",
        "comments_extracted_text",
        "(1)",
    ]  # (1) should be investgated
    for file_path in file_list:
        if all(keyword not in file_path for keyword in exclude_keywords):
            if "comments" in file_path:
                process_comments(bucket, conn, file_path)
            elif "docket" in file_path:
                process_dockets(bucket, conn, file_path)
            elif "documents" in file_path:
                process_documents(bucket, conn, file_path)
            else:
                print(f"Unknown category for file: {file_path}")


def get_s3_files(bucket, docket_id: str):
    agency = get_agency(docket_id)
    files = bucket.objects.filter(
        Prefix=f"{agency}/{docket_id}",
    )
    return [file.key for file in files if file.key.endswith(".json")]


def main():
    # Get docket_id from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python IngestDockets.py <path to file>")
        sys.exit(1)
        
    file_path = sys.argv[1]  
   # print(file_path) 
    with open(file_path, 'r') as file:
        for line in file:
            print(line)
            docket_id = line.strip()
            bucket_name = "mirrulations"
            s3 = boto3.resource(service_name="s3", region_name="us-east-1")

            bucket = s3.Bucket(bucket_name)
            files = get_s3_files(bucket, docket_id)
            sorted_files = sort_files(files)

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
            with psycopg.connect(**conn_params) as conn:
                categorize_and_process_files(bucket, conn, sorted_files)


if __name__ == "__main__":
    main()
