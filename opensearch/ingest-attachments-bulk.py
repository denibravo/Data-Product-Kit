import argparse
import os
import json
from create_client import create_client
import time 


def get_data_from_file(file_path):
    with open(file_path) as file:
        try:
            file_text = file.read()
            method = file_path.split('/')[-2]
            base_name = os.path.basename(file_path)
            comment_id = base_name.split("_attachment")[0]
            docket_id = "-".join(comment_id.split("-")[:-1])
            document = {
                'extractedText': file_text,
                'extractedMethod': method,
                'docketId': docket_id,
                'commentId': comment_id
            }
            return document
        except Exception as e:
            print(f"Error reading file: {file_path}")
            print(e)
            return None

def  bulk_ingest_all(client, directory_name, index_name, ingest_per_bulk, total_to_ingest):
    # the ingest_string will be used to store the bulk ingest request
    ingest_string = ""

    # total_count will keep track of the total number of documents ingested
    total_count = 0
    # bulk_count will keep track of the number of documents in the current bulk request
    bulk_count = 0


    for dirpath, dirnames, filenames in os.walk(directory_name):
        for filename in filenames:
            if "comments_extracted_text" in dirpath and filename.endswith(".txt"):
                document = get_data_from_file(os.path.join(dirpath, filename))
                if not document:
                    continue
                comment_id = document['commentId']
            
                # the action line is used to specify the index name
                action = f'{{"index": {{"_index": "{index_name}", "_id": "{comment_id}"}}}}\n'
                ingest_string += action

                # we get the document from the file and add it to the ingest_string
                ingest_string += json.dumps(document) + '\n'

                # increase both counts by 1
                total_count += 1
                bulk_count += 1

                # if the bulk_count is equal to the ingest_per_bulk, we send the bulk ingest request and reset the bulk_count and ingest_string
                if bulk_count == ingest_per_bulk:
                    try:
                        response = client.bulk(body = ingest_string)
                        print(f"Total documents ingested: {total_count}")
                        bulk_count = 0
                        ingest_string = ""
                    except Exception as e:
                        print(f"Error sending bulk request: {e}")
                        print(ingest_string)
                        print()

    # if there are any documents left in the ingest_string, we send the bulk ingest request
    if ingest_string:
        try:
            print(f"Total documents ingested: {total_count}")
            response = client.bulk(body = ingest_string)
        except Exception as e:
            print(f"Error sending bulk request: {e}")
            print(ingest_string)
            print()

if __name__ == '__main__':
    client = create_client()

    index_name = 'comments_extracted_text'

    # specify the directory name where the JSON files are stored
    
    parser = argparse.ArgumentParser(description='Ingest local comments into Elasticsearch.')
    parser.add_argument('--n_comments', type=int, help='Number of comments to ingest', default=-1)
    parser.add_argument('--time', type=bool, help='Time the ingest', default=False)
    parser.add_argument('--local_directory', type=str, help='Local directory containing JSON files', default='docket-samples')

    directory_name = parser.parse_args().local_directory
    args = parser.parse_args() 
    total_to_ingest = args.n_comments


    if args.time:
        start = time.time()
        
    ingest_per_bulk = 1000
    bulk_ingest_all(client, directory_name, index_name, ingest_per_bulk, total_to_ingest)
    
    if args.time:
        end = time.time()
        print(f"Total time taken: {end - start} seconds")
