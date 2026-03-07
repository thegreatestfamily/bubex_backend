from google.cloud import storage
import os
from django.conf import settings

class CloudStorageService:
    def __init__(self):
        # Path to your service account JSON key
        # In production, this can be set as an environment variable pointing to the file
        self.key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if self.key_path:
            self.client = storage.Client.from_service_account_json(self.key_path)
        else:
            self.client = None

    def download_movie(self, bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        if not self.client:
            raise Exception("Google Cloud Storage client not initialized. Check credentials.")
            
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        return destination_file_name

    def list_movies(self, bucket_name):
        """Lists all the blobs in the bucket."""
        if not self.client:
            return []
            
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs()
        return [blob.name for blob in blobs if blob.name.lower().endswith(('.mp4', '.mkv', '.avi'))]
