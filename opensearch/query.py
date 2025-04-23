from create_client import create_client
import sys

client = create_client()

index_name = "comments"

# Get the search term from the command line
if len(sys.argv) < 2:
    print("Please provide a search term")
    sys.exit(1)

search_term = sys.argv[1]
print(f"Searching for: {search_term}")

query = {
    "size": 0,  # No need to fetch individual documents
    "aggs": {
        "docketId_stats": {
            "terms": {
                "field": "docketId.keyword",  # Use .keyword for exact match on text fields
                "size": 1000000  # Adjust size for expected number of unique docketIds
            },
            "aggs": {
                "matching_comments": {
                    "filter": {
                        "match_phrase": {
                            "commentText": search_term
                        }
                    }
                }
            }
        }
    }
}

# Execute the query
response = client.search(index=index_name, body=query)

# Extract the aggregation results
dockets = response["aggregations"]["docketId_stats"]["buckets"]

# Get the total number of documents in the index
index_stats = client.count(index=index_name)
total_documents = index_stats["count"]

# Create a list of dockets in json format that contains the docketId, docketTitle, the number of total comments, and the number of matching comments out of total comments
dockets = [
    {
        "docketID": docket["key"],
        "doc_count": docket["doc_count"],
        "matching_comments": docket["matching_comments"]["doc_count"]
    }
    
    for docket in dockets
    ]

# Print the list of dockets
print("Dockets:")
for docket in dockets:
    if docket['matching_comments'] > 0:
        print(f"\nDocket ID: {docket['docketID']}")
        print(f"Total comments: {docket['doc_count']}")
        print(f"Matching comments: {docket['matching_comments']}/{docket['doc_count']}")

print(f"\nTotal number of documents in the index: {total_documents}")