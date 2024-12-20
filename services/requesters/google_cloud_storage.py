from google.cloud import storage
import logging

logging.basicConfig(level=logging.INFO)

def read_binary(bucket_name, blob_name):
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your new GCS object
    # blob_name = "storage-object-name"

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        with blob.open("rb") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Failed to read binary data from {bucket_name}/{blob_name}: {e}")
        raise

