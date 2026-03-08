import json
import os
from google.cloud import storage

class CloudStorageService:
    def __init__(self):
        # Support both file path and raw JSON string for Render compatibility
        key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        key_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
        
        try:
            if key_json:
                info = json.loads(key_json)
                self.client = storage.Client.from_service_account_info(info)
            elif key_path:
                self.client = storage.Client.from_service_account_json(key_path)
            else:
                self.client = None
        except Exception as e:
            print(f"Cloud Storage Init Error: {e}")
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
