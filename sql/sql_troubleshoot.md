# SQL Trouble-Shooting Guide

## Connection Errors

If you have previously installed PostgreSQL through homebrew and are encountering connection issues, you may have the PostgreSQL service running in the background on your local machine. 

* To stop the service, run:
```bash
brew services stop postgresql
```

* Ensure Docker is running
    * You can start Docker from the Desktop app or by using the following command:
    ```bash
    open /Applications/Docker.app
    ```

* Check Docker Compose logs:
```bash
docker-compose -f sql/docker-compose.yaml logs sql-client
```

* Verifying PostgreSQL container status:
```bash
docker compose ps
```

## Environment Variable Issues

If you have your `.env` file configured with the correct credentials but are encountering issues with the psql database connection command:

 ```bash
 docker-compose exec sql-client psql -h db -U $POSTGRES_USER -d $POSTGRES_DB
 ```

 Load the `.env` file with your path using the following command:
```bash
source </path/to/your/>.env
```
Test that the environment variables have been correctly set using this command:
```bash
echo $POSTGRES_USER
echo $POSTGRES_DB
```