import argparse
import os
import json
import boto3
from create_client import create_client
import time 


def get_data_from_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
        document = {
            'commentText': data['data']['attributes']['comment'],
            'docketId': data['data']['attributes']['docketId'],
            'commentId': data['data']['id']
        }
        return document

def  bulk_ingest_all(client, directory_name, index_name, ingest_per_bulk, total_to_ingest):
    # the ingest_string will be used to store the bulk ingest request
    ingest_string = ""

    # total_count will keep track of the total number of documents ingested
    total_count = 0
    # bulk_count will keep track of the number of documents in the current bulk request
    bulk_count = 0


    for dirpath, dirnames, filenames in os.walk(directory_name):
        for filename in filenames:
            if dirpath.endswith("comments") and filename.endswith(".json"):
                document = get_data_from_file(os.path.join(dirpath, filename))
                comment_id = document['commentId']
            
                # the action line is used to specify the index name
                action = f'{{"index": {{"_index": "{index_name}", "_id": "{comment_id}"}}}}\n'
                ingest_string += action

                # we get the document from the file and add it to the ingest_string
                ingest_string += json.dumps(document) + '\n'

                # increase both counts by 1
                total_count += 1
                bulk_count += 1

                # if the total_count is equal to the total_to_ingest, we send the bulk ingest request and exit the function
                if total_count == total_to_ingest:
                    response = client.bulk(body = ingest_string)
                    return
                
                # if the bulk_count is equal to the ingest_per_bulk, we send the bulk ingest request and reset the bulk_count and ingest_string
                if bulk_count == ingest_per_bulk:
                    response = client.bulk(body = ingest_string)
                    bulk_count = 0
                    ingest_string = ""

    # if there are any documents left in the ingest_string, we send the bulk ingest request
    if ingest_string:
        response = client.bulk(body = ingest_string)

if __name__ == '__main__':
    client = create_client()

    index_name = 'comments'

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
