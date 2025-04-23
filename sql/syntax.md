
# Tables

## Creation

The script `CreateTables.py` will create the tables and ingest the agency data from the list in *agencies.txt*.

Usage: `docker-compose exec sql-client python CreateTables.py`


## Deletion

The script `DropTables.py` will drop the tables.

Usage: `docker-compose exec sql-client python DropTables.py`

## Reset

The script `ResetDatabase.py` will drop and recreate the tables in one command.

Usage: `docker-compose exec sql-client python ResetDatabase.py`


# Ingest

## Singular Docket

The script `IngestDocket.py` will ingest a given Docket Id, its documents, and comments **from the mirrulations S3 Bucket** into the database.

Example Usage: `docker-compose exec sql-client python IngestDocket.py DOS-2022-0004`

## Multiple Dockets

### From a file

The script `IngestDockets.py` will ingest multiple dockets from a file into the database.


dockets.txt:
```
DOS-2022-0004
FAR-2023-0010
```

Example Usage: `docker-compose exec sql-client python IngestDocket.py dockets.txt`

### From an S3 Bucket

The script `IngestFromBucket.py` will ingest all the dockets from an S3 bucket 

Example Usage: `docker-compose exec sql-client python IngestFromBucket.py BucketName`

### From files stored locally

The script `IngestLocal.py` will ingest all files in a folder.

Example Usage: `docker-compose exec sql-client python IngestLocal.py dockets-data`

## Additional Scripts
- The scripts for Ingesting just comments, dockets, and documents are included for use in current and future scripts, but don't necessarily need to be ran directly in a development environment.

# Query

The script `Query.py` will query the database.

Example Usage: `docker-compose exec sql-client python Query.py "SELECT * FROM dockets;`


# Check Agencies List

The script `CheckAgencies.py` will check the regulations.gov database through the API to see if there are any missing agencies in the `agencies.txt` and update the file if necessary.

Example usage: `docker-compose exec sql-client python CheckAgencies.py`

[You can click here to view rate limits for the regulations.gov API usage.](https://api.data.gov/docs/rate-limits/)