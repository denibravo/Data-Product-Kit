from queries.utils.opensearch import connect as create_client

def query_OpenSearch(search_term):
    client = create_client()
    index_name = "comments"

    query = {
        "size": 0,
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

    response = client.search(index=index_name, body=query)
    dockets = response["aggregations"]["docketId_stats"]["buckets"]

    dockets_list = [
        {
            "id": docket["key"],
            "comments": {
                "match": docket["matching_comments"]["doc_count"],
                "total": docket["doc_count"]
            }
        }
        for docket in dockets if docket["matching_comments"]["doc_count"] > 0
    ]
    
    return dockets_list