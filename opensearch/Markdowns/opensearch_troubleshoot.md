# Opensearch Trouble-Shooting Guide

## Password Strength

If you entered a password that was not strong enough, only the dashboard container will be running.
In order to fix this, the volumes of the nodes must be deleted, and your password must be changed.

1. bring down the docker compose
```bash
docker compose down
```

2. Delete the volumes of the nodes
```bash
docker volume rm opensearch_opensearch-data1 opensearch_opensearch-data2
```

3. Change your `OPENSEARCH_INITIAL_ADMIN_PASSWORD` in your `.env` file to be stronger.

4. Start up the docker compose 
```bash
docker compose up -d
```