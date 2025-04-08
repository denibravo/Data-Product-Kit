from create_client import connect as create_client

def extracted_text_query(search_term):
    
    client = create_client()

    index_name = "comments_extracted_text"

    query = {
        "size": 0,
        "aggs": {
            "docketId_stats": {
                "terms": {
                    "field": "docketId.keyword",  # Use .keyword for exact match on text fields
                    "size": 1000000 # number of matching extracted texts to return
                },
                "aggs": {
                    "matching_attachments": {
                        "filter": {
                            "match_phrase": {
                                    "extractedText": search_term 
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

    # Create a list of comments in json format that contains the commentId, the number of total documents, and the number of matching terms in the extracted text
    dockets_list = [
        {
            "id": docket["key"],
            "attachments": {
                "match": docket["matching_attachments"]["doc_count"],
                "total": docket["doc_count"]
            }
        }
        
        for docket in dockets if docket["matching_attachments"]["doc_count"] > 0
        ]

    return dockets_list