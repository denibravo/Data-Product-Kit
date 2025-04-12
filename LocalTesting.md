# **Local Testing**
**NOTE:** Make sure to have `ENVIRONMENT` as `local` in `.env`
```bash
ENVIRONMENT=local
```

1. **Ingest dockets/documents/comments from S3 into SQL**:
   ```bash
   docker-compose exec sql-client python IngestFromBucket.py <S3_BUCKET_NAME>
   ```

   Example:
   ```bash
   docker-compose exec sql-client python IngestDocket.py docket-samples
   ```

2. **Verify insertion worked (optional)**:
   ```bash
   docker-compose exec sql-client psql -h db -U postgres -d postgres
   ```
   ```bash
   "SELECT * FROM dockets;"
   ```

3. **Ingest comments into OpenSearch**:
   ```bash
   docker exec -it ingest-container bash -c "python -m dp_ingest_local.utils.ingest_opensearch"
   ```
**NOTE:** This script pulls from the s3 bucket in the environment variable --> S3_BUCKET_NAME in `.env`

## Troubleshooting with a Clean Slate

If you're running into unexpected errors, stale data, or inconsistent results, **starting with a clean slate** can help resolve hidden issues.

### Reset Everything (SQL + OpenSearch)

**1. Drop all SQL tables:**
```bash
docker-compose exec sql-client python DropTables.py
```

**2. (Optional) Verify no tables exist:**
```bash
docker-compose exec sql-client psql -h db -U postgres -d postgres
```
```bash
\dt
```
You should see:  
`Did not find any relations.`

**3. Delete OpenSearch indices (like `comments`, `comments_extracted_text`):**
```bash
docker-compose exec ingest python /app/delete_index.py
```
Then type `yes` when prompted.

**4. Recreate fresh tables in SQL:**
```bash
docker-compose exec sql-client python CreateTables.py
```

**5. Re-ingest your data (SQL & OpenSearch):**
```bash
# For SQL:
 docker-compose exec sql-client python IngestFromBucket.py <S3_BUCKET_NAME>

# For OpenSearch:
 docker exec -it ingest-container bash -c "python -m dp_ingest_local.utils.ingest_opensearch"
```

By resetting your data infrastructure this way, you eliminate hidden state that might be causing issues.

## Clean Reset (Optional)
If you want a completely clean slate including everything run:
```bash
docker compose down -v --remove-orphans
docker system prune -af --volumes
```
Then rerun docker:
```bash
docker compose build --no-cache
docker compose up -d
```
Remember to recreate the tables afterwards:
```bash
docker-compose exec sql-client python CreateTables.py 
```