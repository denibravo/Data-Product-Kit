# Use a lightweight Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt from the parent directory
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the Python scripts inside opensearch/
COPY opensearch/ /app/

# Default command to run the ingestion script
CMD ["python", "ingest.py"]
