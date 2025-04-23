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
    ingest(client, 'comments', document)

def ingest_all_comments(client, bucket):
    print("bucket = ", bucket)
    for obj in bucket.objects.all():
        if obj.key.endswith('.json') and ('/comments/' in obj.key):
            ingest_comment(client, bucket, obj.key)

def extract_ids(filename):
    base = os.path.splitext(filename)[0]

    parts = base.split('-')

    docket_id = '-'.join(parts[:3])

    comment_id = docket_id + "-" +parts[3].split('_')[0]

    return docket_id, comment_id

def ingest_pdf_extracted(client, bucket, key):
    obj = bucket.Object(key)
    file_text = obj.get()['Body'].read().decode('utf-8')
    
    base_name = os.path.basename(key)
    docket_id, comment_id = extract_ids(base_name)
    
    document = {
        'extractedText': file_text,
        'extractionMethod': 'pdfminer',
        'docketId': docket_id,
        'commentId': comment_id
    }
    ingest(client, 'comments_extracted_text', document)

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
