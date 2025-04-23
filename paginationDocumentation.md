# Pagination Table Documentation

This documentation describes the structure of the PostgreSQL table that we will use to store the results of a query for use with pagination. The following SQL code creates the table with the desired structur:

```[sql]
CREATE TABLE stored_results (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(), -- when the search is initially made, so we can periodically delete old searches
    -- info about the search: if all of these match, we return corresponding dockets
    search_term TEXT NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    sort_asc BOOLEAN NOT NULL,
    sort_type VARCHAR(20) NOT NULL,
    filter_agencies TEXT NOT NULL, -- comma separated, alphabetical order, empty string for no filter
    filter_date_start TIMESTAMP WITH TIME ZONE NOT NULL,
    filter_date_end TIMESTAMP WITH TIME ZONE NOT NULL,
    filter_rulemaking VARCHAR(15) NOT NULL, -- empty string for no filter
    -- info about the docket
    search_rank INT NOT NULL,
    docket_id VARCHAR(50) NOT NULL,
    total_comments INT NOT NULL,
    matching_comments INT NOT NULL,
    relevance_score FLOAT NOT NULL
)
```

After a search is made with `refreshResults=True`, we add the top 100 dockets to the table. All will have the same stored info about the search, and `search_rank` will go from 0 to 99. 

If `refreshResults=False` and we request page $n$ (where $n$ is in the range $[0, 9]$), we return dockets that match all fields with search data and rank in the interval $[10n, 10n+9]$.

Note that we store when the search is initially made. This way, we can periodically go through and drop all entries that are older than a certain interval.