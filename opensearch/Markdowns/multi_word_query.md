# This is documentation for OpenSearch on how to perform multi-word queries.


## Single-word query
- Note: This was done initially in the project and believed to be correct. Until during manual testing and examination of docket results, it was found that the results were not as expected. This form of the OpenSearch Query would search for the first word entered into the search bar and return results for that word only. It was also found that if the words "AND" or "OR" were used, the results would return all documents that contained either of those words. This was not the expected behavior. The expected behavior was to return results that contained both words. This was later confirmed to be the case in the OpenSearch documentation.

### Example:
query = {
    "size": 0,  # No need to fetch individual documents
    "aggs": {
        "docketId_stats": {
            "terms": {
                "field": "docketId.keyword",  # Use .keyword for exact match on text fields
                "size": 1000  # Adjust size for expected number of unique docketIds
            },
            "aggs": {
                "matching_comments": {
                    "filter": {
                        "match": {
                            "commentText": "drug"
                        }
                    }
                }
            }
        }
    }
}

### Note:
- This query will return the count of documents for each unique docketId that contains the word "drug" in the commentText field.
- But if you want to search for multiple words, this query will not work as expected.

# Multi-word query:
- The changes to this are the that instead of using the "match" query, we will use the "match_phrase" query. This will ensure that the words are searched for in the order they are entered into the search bar. This will also ensure that the results returned will be for documents that contain all of the words entered into the search bar. This was confirmed to be the case in the OpenSearch documentation. Also we had to change the size of the results returned to 1000000. This was done to ensure that all of the results were returned and viewable.

## Example:

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

## For further questions on queries, please refer to the OpenSearch documentation:
https://opensearch.org/docs/latest/query-dsl/full-text/index/