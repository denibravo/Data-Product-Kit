import os
import json
from create_client import create_client


def ingest(client, document):
    """Indexes a document into the Elasticsearch cluster."""
    try:
        response = client.index(index='comments', body=document)
   #     print(f"Indexed document {document['commentId']}: {response}")
    except Exception as e:
        print(f"Error indexing document {document.get('commentId', 'unknown')}: {e}")


def ingest_local_comment(client, file_path):
    """Reads a local JSON file and ingests it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        document = {
            'commentText': data['data']['attributes'].get('comment', ''),
            'docketId': data['data']['attributes'].get('docketId', ''),
            'commentId': data['data'].get('id', '')
        }

        ingest(client, document)
    except Exception as e:
        print(f"Error processing local file {file_path}: {e}")


def ingest_n_local_comments(client, directory, n_comments):
    """Processes up to 'n_comments' JSON files from the local directory."""
    file_paths = []

    try:
        # Collecting all valid file paths
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.json') and '/comments/' in file_path.replace("\\", "/"):
                    file_paths.append(file_path)

        # Determine the number of files to ingest
        total_to_ingest = len(file_paths) if n_comments == -1 else min(n_comments, len(file_paths))

        # Ingest the files
        for i in range(total_to_ingest):
            ingest_local_comment(client, file_paths[i])

        # print(f"Ingested {total_to_ingest} comments from local directory.")

    except Exception as e:
        print(f"Error processing local directory {directory}: {e}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Ingest local comments into Elasticsearch.')
    parser.add_argument('n_comments', type=int, help='Number of comments to ingest', default=-1)
    parser.add_argument('time', type=float, help='Time taken to ingest', default=False)
    parser.add_argument('local_directory', type=str, help='Local directory containing JSON files", default="docket-samples')
    args = parser.parse_args()

    client = create_client()
    local_directory = args.local_directory

    if not os.path.exists(local_directory):
        print(f"Error: Local directory '{local_directory}' does not exist.")
    else:

        import time
        start = time.time()
        ingest_n_local_comments(client, local_directory, args.n_comments)
        end = time.time()
        print(f"Time taken: {end - start:.2f} seconds for {args.n_comments} comments.")