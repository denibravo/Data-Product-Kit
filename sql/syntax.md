
# Tables

## Creation

The script `CreateTables.py` will create the tables.

Usage: `python3 CreateTables.py`


## Deletion

The script `DropTables.py` will drop the tables.

Usage: `python3 DropTables.py`

## Reset

The script `ResetDatabase.py` will drop and recreate the tables in one command.

Usage: `python3 ResetDatabase.py`


# Ingest

## Singular Docket

The script `IngestDocket.py` will ingest a given Docket Id, its documents, and comments **from the mirrulations S3 Bucket** into the database.

Example Usage: `python3 IngestDocket.py DOS-2022-0004`

## Multiple Dockets

### From a file

The script `IngestDockets.py` will ingest multiple dockets from a file into the database.


dockets.txt:
```
DOS-2022-0004
FAR-2023-0010
```

Example Usage: `python3 IngestDocket.py dockets.txt`

### From an S3 Bucket

The script `IngestFromBucket.py` will ingest all the dockets from an S3 bucket 

Example Usage: `python3 IngestFromBucket.py BucketName`

### From files stored locally

The script `IngestLocal.py` will ingest all files in a folder.

Example Usage: `python3 IngestLocal.py dockets-data`

## Additional Scripts
- The scripts for Ingesting just comments, dockets, and documents are included for use in current and future scripts, but don't necessarily need to be ran directly in a development environment.

# Query

The script `Query.py` will query the database.

Example Usage: `python3 Query.py "SELECT * FROM dockets;`