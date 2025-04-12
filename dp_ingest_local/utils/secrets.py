import os

def get_secret(secret_name):
    """
    Local-only secret loader for development/testing inside Docker.
    Reads values from .env or environment variables.
    """

    print(f"[LOCAL get_secret] Requested secret: {secret_name}")

    if "postgres" in secret_name:
        return {
            "username": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "engine": "postgres",
            "host": os.getenv("POSTGRES_HOST"),
            "port": int(os.getenv("POSTGRES_PORT")),
            "db": os.getenv("POSTGRES_DB")
        }

    elif "opensearch" in secret_name:
        return {
            "host": os.getenv("OPENSEARCH_HOST"),
            "port": int(os.getenv("OPENSEARCH_PORT")),
            "password": os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD")
        }

    raise ValueError(f"[LOCAL get_secret] Unknown secret name: {secret_name}")
