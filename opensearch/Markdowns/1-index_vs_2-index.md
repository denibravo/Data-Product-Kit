# 1-Index vs. 2-Index Approaches

## 1-Index Approach (Single Index)

- **Structure:**  
  Both parent and child documents are stored in one index.

- **Notes:**  
  - Native support for parent–child queries
  - Simplifies querying because all related data is in the same index.

- **Considerations:**  
  - A larger single index can affect performance, especially with complex join queries.

---

## 2-Index Approach (Separate Indexes)

- **Structure:**  
  Parent documents are stored in one index and child documents in another.

- **Notes:**  
  There is no native join capability across separate indexes in OpenSearch.

- **Considerations:**  
  - You have to handle joins externally, typically by issuing multiple queries and merging results.
  - This adds complexity and may not perform as well as the built-in join features available with the 1-index approach.

---

## Parent–Child Joins on a Single Index (> 100MB)

- **Feasibility:**  
  You can use a parent–child join on a single index regardless of its size,even if it is larger than 100MB.

- **Considerations:**  
  - There’s no inherent limitation on the size of an index for using parent–child relationships, performance can be impacted as the index grows.
  - Large indices may lead to slower query response times if not optimized properly.

---

## Parent–Child Joins on a Two-Index (> 100MB)

- **Feasibility:**  
  Native parent–child join queries are not supported across separate indexes in OpenSearch. You need to create a more complex queries, which makes it less practical for larger datasets.

- **How-To:**  
  - Retrieve parent documents from one index.
  - Retrieve child documents from another index.
  - Merge or correlate the results.

- **Considerations:**  
  - This will probably introduce additional complexity and performance overhead.
  - Synchronizing data and maintaining consistency between the indexes will become a challenge.