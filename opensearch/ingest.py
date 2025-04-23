import os
import json
import boto3


def ingest(client, document):
    response = client.index(index = 'comments', body = document)
   # print(response)

def ingest_comment(client, bucket, key):
    obj = bucket.Object(key)
    file_text = obj.get()['Body'].read().decode('utf-8')
    data = json.loads(file_text)
    document = {
        'commentText': data['data']['attributes']['comment'],
        'docketId': data['data']['attributes']['docketId'],
        'commentId': data['data']['id']
    }
    ingest(client, document)

def ingest_all_comments(client, bucket):
    print("bucket = ", bucket)
    for obj in bucket.objects.all():
        if obj.key.endswith('.json') and ('/comments/' in obj.key):
            ingest_comment(client, bucket, obj.key)


if __name__ == '__main__':
    from create_client import create_client
    client = create_client()

    s3 = boto3.resource(
        service_name = 's3',
        region_name = 'us-east-1'
    )

    print('boto3 created')

    bucket = s3.Bucket(os.getenv('S3_BUCKET_NAME'))
    # ingest_all_comments(client, bucket)
