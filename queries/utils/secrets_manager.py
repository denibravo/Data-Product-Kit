import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

def get_secret(secret_name):
    """
    Retrieve a secret from AWS Secrets Manager or fall back to local .env variables.
    Defaults to local unless ENVIRONMENT=prod is set.
    """
    environment = os.getenv("ENVIRONMENT").lower()
    print(f"[DEBUG] ENVIRONMENT = {environment}")

    if environment != "prod":
        print(f"[INFO] Using local fallback for secret: {secret_name}")
        load_dotenv()
        if 'opensearch' in secret_name:
            return {
                "host": os.getenv("OPENSEARCH_HOST"),
                "port": os.getenv("OPENSEARCH_PORT", "9200")
            }

        if 'postgres' in secret_name:
            return {
                "username": os.getenv("POSTGRES_USER"),
                "password": os.getenv("POSTGRES_PASSWORD"),
                "engine": "postgres",
                "host": os.getenv("POSTGRES_HOST"),
                "port": os.getenv("POSTGRES_PORT"),
                "dbClusterIdentifier": "local",
                "db": os.getenv("POSTGRES_DB")
            }

        raise Exception(f"Unknown local secret requested: {secret_name}")

    # Production path — use AWS Secrets Manager
    print(f"[INFO] Using AWS Secrets Manager for secret: {secret_name}")
    region_name = os.environ.get('AWS_REGION', 'us-east-1')

    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)

        response = client.get_secret_value(SecretId=secret_name)
        print(response)

        if 'SecretString' in response:
            return json.loads(response['SecretString'])
        else:
            raise Exception("Secret not found in expected format")

    except ClientError as e:
        print(f"[ERROR] Failed to retrieve secret from AWS: {e}")
        raise e
