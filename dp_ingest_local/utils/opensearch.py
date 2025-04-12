import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch
import certifi

def connect():
    load_dotenv()

    host = os.getenv("OPENSEARCH_HOST")
    port = int(os.getenv("OPENSEARCH_PORT"))
    password = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD")

    print(f"[DEBUG] Connecting to OpenSearch @ {host}:{port} with password: {password[:3]}***")

    if not host or not port or not password:
        raise ValueError("Missing OPENSEARCH_* values in environment")

    # Basic auth (admin:password)
    auth = ("admin", password)

    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,
        http_auth=auth,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        ca_certs=certifi.where()
    )

    return client
