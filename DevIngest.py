import opensearch.ingest as ingest
import sql.IngestDockets as IngestDockets
from opensearch.create_client import create_client
import boto3 


SAMPLE_DOCKETS = [
     "FDA/FDA-2023-N-0437", #too many comments, (34k)
    "CMS/CMS-2024-0111",  # ~50
    "FDA/FDA-2021-P-0558",  # ~750
    "FDA/FDA-2017-D-6352",  # 818
     "FAA/FAA-2019-1100", #too many comments (54k)
     "CEQ/CEQ-2025-0002", #88k
     "ED/ED-2023-OPE-0004", #13k
     "DEA/DEA-2023-0029", #41k
     "CMS/CMS-2024-0345", #30k
     "USCIS-2021-0010", #7k
     "USCIS/IRS-2023-0066", #30k
     "CMS/CMS-2025-0020", #25k
     "IRS/IRS-2020-0016", #12k
     "FDA/FDA-2015-N-0030", #55k
     "HHS/HHS-OS-2011-0020",  # 2k / prob not
    "FDA/FDA-2023-D-1955",  # 46
    "FDA/FDA-2015-N-3469",  # 44
    "CMS/CMS-2018-0133",  # 261
     "CDC/CDC-2024-0103",  # 1200
     "TB/TB-2024-0002", #5k / prob not
     "CMS/CMS-2025-0020", #25k
     "DEA/EA-2024-0120",  # 1880 / prob not
     "HHS/HHS-OS-2022-0012", #73k
     "CFPB/CFPB-2015-0021", #8k
    "DOS/DOS-2014-0003", #127k
    "FMCSA/FMCSA-2013-0124",  # 6
     "FWS/FWS-R7-NWRS-2023-0072", #79k
     "FTC/FTC-2023-0007", #20k
     "FTC/FTC-2024-0022",  # 2k / prob not
    "WHD/WHD-2022-0003", #54k
     "EEOC/EEOC-2023-0004", #100k
    "EPA/EPA-HQ-OPP-2024-0431",  # 420
    "DOT/DOT-OST-2024-0062",  # 344
     "WHD/WHD-2022-0003", #54k
     "VA/VA-2022-VHA-0021",#57k
    "EPA/EPA-HQ-OAR-2023-0589",
    "DOT/DOT-OST-2025-0026",
    "OPM/OPM-2024-0016",
    "FAA/FAA-2024-1395",
    "USCIS/USCIS-2007-0024",
    "FDA/FDA-2015-D-3517",
    "HHS/HHS-OASH-2024-0019",
]

def IngestLocalOpenSearch():
    """
    Ingests data from an s3 bucket to a local OpenSearch instance.
    """
    # dockets Change this to the dockets you want to ingest

    client  = create_client()


    s3 = boto3.resource(
        service_name = 's3',
        region_name = 'us-east-1'
    )

 #   bucket = s3.Bucket('mirrulations')
    bucket = s3.Bucket('mirrulations')
 #  print(bucket.objects.all())
    for docket in SAMPLE_DOCKETS:
        print(docket)
        # Get the files for the docket and call ingest(client,document)
        for obj in bucket.objects.filter(Prefix = f'raw-data/{docket}/'):
           # print("obj.key = ", obj.key)
            if obj.key.endswith('.json') and (f'{docket}/comments/' in obj.key):
                ingest.ingest_comment(client, bucket, obj.key)
                print("Ingested comment from: ", obj.key)

    
def IngestSQL():
    """
    Ingests data from S3 to SQL.
    """
    import sys

    #trick main to think that sys.argv is being passed (very hacky, but it works)
    sys.argv = ['IngestDockets.py', 'dockets.txt']
    IngestDockets.main()
    


if __name__ == "__main__":
    IngestSQL()