folders=(
CDC
)
# 
mkdir -p IngestAttachmentLogs
for folder in "${folders[@]}"
do
    echo "Starting Attachment Ingest for $folder" >>IngestAttachments.log 
    python  -u ingest-attachments-bulk.py --local_directory=../../mirrulations/$folder/ >IngestAttachmentLogs/$folder.log 
    echo "Finished Attachment Ingest for $folder"  >>IngestAttachments.log
done