t"""
This script deletes  indexes from OpenSearch. It prompts the user for confirmation before deleting the index.
It uses the OpenSearch client created in create_client.py.
Authors: Data Product Team Spring 2025
"""
from create_client import create_client


client = create_client()

indices = ['comments']

host = client.transport.hosts
print(host)

for index in indices:
    print(f"Deleting index '{index}' from {host}. Type 'yes' to confirm.")
    confirm = input()
    if confirm == 'yes':
        client.indices.delete(index=index, ignore=[400, 404])
        print(f"Index '{index}' deleted.")
    else:
        print(f"Index '{index}' not deleted.")