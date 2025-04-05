import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

def get_secret(secret_name):
    """
    Retrieve a secret from AWS Secrets Manager
    Args:
        secret_name: Name of the secret to retrieve
    Returns:
        dict: The secret key/value pairs
    """    
    load_dotenv()

    opensearch_host = os.environ.get('OPENSEARCH_HOST', '')
    if opensearch_host == 'opensearch-node1':
        print(f"[INFO] Using local fallback for secret: {secret_name}")

        if 'opensearch' in secret_name:
            return {
                "host": os.environ.get("OPENSEARCH_HOST"),
                "port": os.environ.get("OPENSEARCH_PORT", "9200")
            }

        if 'postgres' in secret_name:
            return {
                "username": os.environ.get("POSTGRES_USER"),
                "password": os.environ.get("POSTGRES_PASSWORD"),
                "engine": "postgres",
                "host": os.environ.get("POSTGRES_HOST"),
                "port": os.environ.get("POSTGRES_PORT"),
                "dbClusterIdentifier": "local",
                "db": os.environ.get("POSTGRES_DB")
            }

        raise Exception(f"Unknown local secret requested: {secret_name}")

    region_name = os.environ.get('AWS_REGION', 'us-east-1')

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Get the secret value
        response = client.get_secret_value(SecretId=secret_name)
        print(response)

        # Decode and parse the secret string JSON
        if 'SecretString' in response:
            secret = json.loads(response['SecretString'])
            return secret
        else:
            print("Secret not found in expected format")
            raise Exception("Secret not found in expected format")

    except ClientError as e:
        print(f"Error retrieving secret: {str(e)}")
        raise e