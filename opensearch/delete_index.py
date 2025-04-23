t"""
This script deletes  indexes from OpenSearch. It prompts the user for confirmation before deleting the index.
It uses the OpenSearch client created in create_client.py.
Authors: Data Product Team Spring 2025
"""
from create_client import create_client
import argparse


client = create_client()

indices = ['comments']

host = client.transport.hosts
#print(host)

parser = argparse.ArgumentParser(description='Delete indices from OpenSearch.')
parser.add_argument('--yes', action='store_true', help='Automatically confirm deletion of indices.')
args = parser.parse_args()

for index in indices:
    if args.yes:
        confirm = 'yes'
    else:
        print(f"Deleting index '{index}' from {host}. Type 'yes' to confirm.")
        confirm = input()
    
    if confirm == 'yes':
        client.indices.delete(index=index, ignore=[400, 404])
#        print(f"Index '{index}' deleted.")
    else:
        print(f"Index '{index}' not deleted.")