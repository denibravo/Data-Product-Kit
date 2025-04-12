import os
import json
import boto3
from .opensearch import connect as create_client


def ingest_comment_from_text(client, content):
    data = json.loads(content)
    document = {
        'commentText': data['data']['attributes']['comment'],
        'docketId': data['data']['attributes']['docketId'],
        'commentId': data['data']['id']
    }
    ingest(client, document, id = document['commentId'], index= 'comments')

def ingest(client, document, id, index):
    print(f"[Ingest] Indexing to: {index}, ID: {id}")
    try:
        res = client.index(index=index, body=document, id=id)
        print(f"[Ingest Success] Response: {res}")
    except Exception as e:
        print(f"[Ingest ERROR] Failed to index doc {id} into {index}")
        print(e)


def ingest_extracted_text_from_text(client, data):

    document = {
        'extractedText': data['extractedText'],
        'extractedMethod': data['extractedMethod'],
        'docketId': data['docketId'],
        'commentId': data['commentId'],
        'attachmentId': data['attachmentId']
    }
    ingest(client, document, id = document['commentId'], index= 'extracted_text_test')


def ingest_comment(client, bucket, key):
    obj = bucket.Object(key)
    file_text = obj.get()['Body'].read().decode('utf-8')
    data = json.loads(file_text)
    document = {
        'commentText': data['data']['attributes']['comment'],
        'docketId': data['data']['attributes']['docketId'],
        'commentId': data['data']['id']
    }
    ingest(client, document, id=document["commentId"], index="comments") 

def ingest_pdf_extracted(client, bucket, key):
    obj = bucket.Object(key)
    file_text = obj.get()['Body'].read().decode('utf-8')

    # Build ID logic (can be adjusted if needed)
    base = os.path.basename(key)
    parts = base.replace(".json", "").split("-")
    docket_id = "-".join(parts[:3])
    comment_id = docket_id + "-" + parts[3].split("_")[0]

    document = {
        'extractedText': file_text,
        'extractionMethod': 'pdfminer',
        'docketId': docket_id,
        'commentId': comment_id
    }

    ingest(client, document, id=comment_id, index="comments_extracted_text")

def ingest_all_comments(client, bucket):
    for obj in bucket.objects.all():
        if obj.key.endswith('.json') and ('/comments/' in obj.key):
            ingest_comment(client, bucket, obj.key)

def ingest_all_extracted_text(client, bucket):
    for obj in bucket.objects.all():
        if obj.key.endswith('.txt') and 'comments_extracted_text' in obj.key:
            ingest_pdf_extracted(client, bucket, obj.key)

if __name__ == '__main__':
    client = create_client()

    s3 = boto3.resource(
        service_name = 's3',
        region_name = 'us-east-1'
    )

    print('boto3 created')

    bucket = s3.Bucket(os.getenv('S3_BUCKET_NAME'))

    ingest_all_comments(client, bucket)
    ingest_all_extracted_text(client, bucket)
