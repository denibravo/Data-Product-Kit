# Data-Product-Kit
A guide to acquire, install and deploy the search capability via API, for SQL and OpenSearch.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
    * If you encounter issues with Docker, try uninstalling and reinstalling it using Homebrew:
    ```bash
    brew uninstall --cask docker --force
    brew uninstall --formula docker --force
    brew install --cask docker
    ```
    * This works even if Docker was not originally installed using Homebrew.

- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/)
- [libpq](https://www.postgresql.org/docs/current/libpq.html#:~:text=libpq%20is%20the%20C%20application,the%20results%20of%20these%20queries.)
    - Install `libpq` via Homebrew:
    ```bash
    brew install libpq
    brew link --force libpq
    ```

- [Regulations.gov API Key](https://open.gsa.gov/api/regulationsgov/)
   - Register for an API key at the top of the page

## Initial Setup

Clone the `Data-Product-Kit` repository:
```bash
git clone https://github.com/mirrulations/Data-Product-Kit.git
```

Create a virtual environment, activate it, and install the requirements:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make sure to initiate the submodule:
```bash
git submodule update --init
```

## Setting Up the Environment Variables

Create a `.env` file in the parent directory with the following fields:
```bash
OPENSEARCH_INITIAL_ADMIN_PASSWORD=<your_secure_password>
OPENSEARCH_HOST=opensearch-node1
OPENSEARCH_PORT=9200
S3_BUCKET_NAME=presentationbucketcs334s25
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
REGULATIONS_API_KEY=<your_API_key>
```
**NOTE:** For OpenSearch including a `$` or a `!` in the password as a special character may lead to issues when running docker compose later on (the following text gets interpreted as a shell variable), so avoid using them in your password.

**NOTE:** When running locally, you can set the username and password to any desired credentials. **Example credentials are included below:**

```bash
OPENSEARCH_INITIAL_ADMIN_PASSWORD=C4nzUMkFu^e4N2
OPENSEARCH_HOST=opensearch-node1
OPENSEARCH_PORT=9200
S3_BUCKET_NAME=presentationbucketcs334s25
```
**NOTE:** <ins>The S3 Bucket we are using for sample data is `presentationbucketcs334s25`</ins>. You can use your own bucket by changing the value of S3_BUCKET_NAME in the `.env` file.

Run the following command to load the environment variables:
```bash
source .env
```

# Docker Network
We now use a Docker network that allows OpenSearch and SQL to communicate within containers without being exposed to the local machine.

## Starting Services

1. **Ensure Docker is running.**
2. Start all services (OpenSearch, SQL, and Query):
   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```
**NOTE:** This should run a total of 7 containers, as well as running the Docker Network 

3. Verify running containers:
   ```bash
   docker compose ps
   ```
**Note:** There should be 3 opensearch containers running upon successful execution. If you are having issues, you may want to revisit your password as the containers will not start with a low strength password. [Visit the OpenSearch troubleshooting guide for further assistance.](opensearch/opensearch_troubleshoot.md)

```bash
docker-compose exec opensearch-node1 curl -X GET "http://opensearch-node1:9200"  
```

# OpenSearch

## Using OpenSearch

1. In the virtual environment, run the following command to create the index and ingest the data:
   ```bash
   docker-compose exec ingest python /app/ingest.py
   ```
   **Note:** This may take a few minutes.

2. To query the data, run the following command:
   ```bash
   docker-compose exec ingest python /app/query.py <search_term>
   ```
   **Note:** Only dockets with matching comments will appear in the output.

## Cleanup

1. To delete data from the OpenSearch instance, run the following command: 
   ```bash
   docker-compose exec ingest python /app/delete_index.py
   ```

# SQL

### **Troubleshooting tips are available in the <u>[SQL Troubleshooting Guide](sql/sql_troubleshoot.md](https://github.com/mirrula**tions/Data-Product-Kit/blob/main/sql/sql_troubleshoot.md))</u>**

## Using SQL

1. **Create Tables & Insert Data:**
   ```bash
   docker-compose exec sql-client python CreateTables.py
   ```

2. **Ingest Data from S3 Bucket:**
   ```bash
   docker-compose exec sql-client python IngestFromBucket.py presentationbucketcs334s25
   ```

3. **Optional: Ingest Individual Docket from Mirrulations S3 Bucket:**
   ```bash
   docker-compose exec sql-client python IngestDocket.py <docket_id>
   ```
   **Example Docket:** `DOS-2022-0004`

4. **Optional: Ingest Agency Data From regulations.gov:**

   To check for and insert missing agency data into the `agencies.txt` file, run:
   ```bash
   docker-compose exec sql-client python CheckAgencies.py
   ```

**IMPORTANT:** Additional documentation for all the scripts for SQL can be found [here](sql/syntax.md)

### Querying SQL

1. **PSQL Interface:**
   ```bash
   docker-compose exec sql-client psql -h db -U postgres -d postgres
   ```
    You can begin querying once the connection has been established. 


   To enhance readability:
   ```bash
   \x
   ```
   Exit PSQL:
   ```bash
   \q
   ```

2. **Query Using Script:**
    * This command allows the user to input a SQL query:
   ```bash
   docker-compose exec sql-client python /app/Query.py "SELECT docket_id FROM dockets;"
   ```

 An example query is provided above. 

**NOTE:** Queries are limited to SELECT statements and must be written within the quotation marks.The script must be rerun per query issued; output is returned in JSON format.

## Cleanup

1. **Drop Tables:**
   ```bash
   docker-compose exec sql-client python DropTables.py
   ```

# Querying Both OpenSearch & SQL

To run a search query that integrates both OpenSearch and SQL:
```bash
docker compose exec queries python query.py "<search_term>"
```

This will:
1. Query OpenSearch for docket IDs matching the search term.
2. Fetch additional details from SQL for those docket IDs.
3. Return combined results.

# Stop the Containers
To stop the docker containers, run the following command:
```bash
docker compose down
```

For additional help, reach out to the Data Product team.

