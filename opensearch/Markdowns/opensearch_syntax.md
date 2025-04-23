# OpenSearch Syntax Documentation

## Overview
This document provides an overview of OpenSearch syntax, including querying data, filtering results, and interacting with OpenSearch using SQL, Piped Processing Language (PPL), and DSL queries. The primary focus is on querying the `comments` index to retrieve and analyze public comments from different dockets.

---

## 1. Querying Data Using SQL
OpenSearch supports SQL queries through the `_plugins/_sql` endpoint, which allows users to write queries in SQL syntax for easy data retrieval.

### Example SQL Query
```json
POST _plugins/_sql
{
  "query": "SELECT * FROM comments LIMIT 50"
}
```

### Querying Comments by Docket ID
```json
POST _plugins/_sql
{
  "query": "SELECT * FROM comments WHERE docketId = 'FDA-2024-XYZ' LIMIT 20"
}
```

### Aggregating Comment Counts by Docket ID
```json
POST _plugins/_sql
{
  "query": "SELECT docketId, COUNT(*) AS comment_count FROM comments GROUP BY docketId"
}
```

---

## 2. Querying Data Using PPL (Piped Processing Language)
PPL allows querying in a pipeline (`|`) format, making it intuitive for data filtering and aggregation.

### Example PPL Query
```json
POST _plugins/_ppl
{
  "query": "source=comments | fields docketId, comment | head 50"
}
```

### Finding Comments Containing a Specific Keyword
```json
POST _plugins/_ppl
{
  "query": "source=comments | where comment like 'drug' | fields docketId, comment"
}
```

---

## 3. Querying Data Using DSL (Domain-Specific Language)
OpenSearch also supports querying via JSON-based DSL, offering more flexibility for complex queries.

### Example DSL Query for Keyword Matching
```json
POST comments/_search
{
  "query": {
    "match": {
      "comment": "drug"
    }
  }
}
```

### Aggregation by Docket ID with Matching Keyword
```json
POST comments/_search
{
  "size": 0,
  "aggs": {
    "docket_counts": {
      "terms": {
        "field": "docketId.keyword",
        "size": 100
      },
      "aggs": {
        "matching_comments": {
          "filter": {
            "match": {
              "comment": "drug"
            }
          }
        }
      }
    }
  }
}
```

---

## 4. Pagination and Deep Pagination
To retrieve large datasets, OpenSearch allows pagination using `LIMIT` and `OFFSET`.

### Example Query with Pagination
```json
POST _plugins/_sql
{
  "query": "SELECT * FROM comments LIMIT 50 OFFSET 100"
}
```

For deep pagination, `search_after` is recommended instead of `from` and `size` to optimize performance.

### Example Deep Pagination Query
```json
POST comments/_search
{
  "size": 50,
  "query": {
    "match_all": {}
  },
  "search_after": ["last_sort_value"]
}
```

---

## 5. Managing Indexes
Indexes in OpenSearch act as containers for structured data storage.

### Create an Index
```json
PUT comments
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
```

### Delete an Index
```json
DELETE comments
```

### List All Indexes
```json
GET _cat/indices?v
```

---

## 6. Managing Documents
Documents in OpenSearch represent individual records within an index.

### Insert a Comment Document
```json
POST comments/_doc/
{
  "comment": "This is an important regulation.",
  "docketId": "EPA-2025-XYZ",
  "author": "John Doe",
  "modifyDate": "2025-02-04"
}
```

### Update a Document
```json
POST comments/_update/1
{
  "doc": {
    "comment": "Updated comment text."
  }
}
```

### Delete a Single Document
```json
DELETE comments/_doc/1
```

### Delete All Documents Matching a Query
```json
POST comments/_delete_by_query
{
  "query": {
    "match": { "docketId": "FDA-2024-XYZ" }
  }
}
```

---

## 7. Authentication and Endpoints
### Local Deployment (Docker-based OpenSearch)
- **Endpoint:** `https://localhost:9200`
- **Authentication:** Username: `admin`, Password: `$OPENSEARCH_INITIAL_PASSWORD`
- **Example Query via `curl`**:
```sh
curl -XPOST https://localhost:9200/comments/_search -u admin:$OPENSEARCH_INITIAL_PASSWORD -H "Content-Type: application/json" -d '{"query":{"match_all":{}}}'
```

### Cloud Deployment (AWS OpenSearch Serverless)
- **Endpoint:** `https://<your-opensearch-endpoint>`
- **Authentication:** Uses AWS IAM Role-based authentication
- **Example Query via Python (`opensearch-py`)**:
```python
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

host = "<your-opensearch-endpoint>"
region = "us-east-1"
credentials = boto3.Session().get_credentials()
auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, "aoss", session_token=credentials.token)

client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

response = client.search(index="comments", body={"query": {"match_all": {}}})
print(response)
```

---

## Summary
- OpenSearch supports SQL queries via `_plugins/_sql`, PPL via `_plugins/_ppl`, and JSON-based DSL queries.
- Pagination can be handled via `LIMIT`, `OFFSET`, and `search_after` for deep pagination.
- Index management includes creating, deleting, and listing indexes.
- Document management allows inserting, updating, and deleting records efficiently.
- Authentication differs for **local (Docker)** vs **cloud (AWS OpenSearch Serverless)**.
