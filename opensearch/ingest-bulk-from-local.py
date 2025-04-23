import os
import json
import boto3
from create_client import create_client

def get_data_from_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
        document = {
            'commentText': data['data']['attributes']['comment'],
            'docketId': data['data']['attributes']['docketId'],
            'commentId': data['data']['id']
        }
        return document

def bulk_ingest_all(client, directory_name, index_name, ingest_per_bulk, total_to_ingest):
    # the ingest_string will be used to store the bulk ingest request
    ingest_string = ""

    # total_count will keep track of the total number of documents ingested
    total_count = 0
    # bulk_count will keep track of the number of documents in the current bulk request
    bulk_count = 0


    for dirpath, dirnames, filenames in os.walk(directory_name):
        for filename in filenames:
            if dirpath.endswith("comments") and filename.endswith(".json"):
                # the action line is used to specify the index name
                action = f'{{"index": {{"_index": "{index_name}"}}}}\n'
                ingest_string += action

                # we get the document from the file and add it to the ingest_string
                document = get_data_from_file(os.path.join(dirpath, filename))
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

    index_name = 'comments_bulk_test'

    # specify the directory name where the JSON files are stored
    directory_name = "docket-samples"
    # specify the total number of documents to ingest
    # use -1 to ingest all documents in the directory
    total_to_ingest = -1
    # specify the number of documents to ingest per bulk request
    # NOTE: this can likely be optimized, but for now we will use 1000
    ingest_per_bulk = 1000

    bulk_ingest_all(client, directory_name, index_name, ingest_per_bulk, total_to_ingest)