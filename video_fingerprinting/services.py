import cv2
import numpy as np
import os
from django.conf import settings
from .models import VideoFingerprint
from .cloud_storage import CloudStorageService

class FingerprintService:
    @staticmethod
    def _calculate_dhash(image, hash_size=8):
        """
        Calculate the difference hash for a given image.
        """
        # Resize the image to hash_size + 1 x hash_size and convert to grayscale
        resized = cv2.resize(image, (hash_size + 1, hash_size))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # Calculate the difference between adjacent pixels
        diff = gray[:, 1:] > gray[:, :-1]
        
        # Convert the boolean array to a hexadecimal string
        return "".join([f"{int(b):x}" for b in diff.flatten()])

    @classmethod
    def generate_fingerprints(cls, video_path, interval_seconds=1.0):
        """
        Generate fingerprints for a video file at given intervals.
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            return []
            
        frame_interval = int(fps * interval_seconds)
        fingerprints = []
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                timestamp = frame_count / fps
                dhash = cls._calculate_dhash(frame)
                fingerprints.append({
                    'timestamp': timestamp,
                    'hash': dhash
                })
                
            frame_count += 1
            
        cap.release()
        return fingerprints

    @classmethod
    def save_movie_fingerprints(cls, movie, video_path):
        """
        Process a movie file and save its fingerprints to the database.
        """
        fingerprints = cls.generate_fingerprints(video_path)
        
        # Clean up existing fingerprints for this movie to avoid duplicates
        VideoFingerprint.objects.filter(movie=movie).delete()
        
        VideoFingerprint.objects.create(
            movie=movie,
            fingerprint_data={'hashes': fingerprints},
            start_time_offset=0,
            duration=len(fingerprints)
        )

    @classmethod
    def process_cloud_movie(cls, movie):
        """
        Downloads a movie from GCS, fingerprints it, and cleans up.
        """
        if not movie.cloud_bucket or not movie.cloud_file_path:
            return False
            
        cloud_service = CloudStorageService()
        temp_file = f"temp_{movie.id}_{os.path.basename(movie.cloud_file_path)}"
        
        try:
            cloud_service.download_movie(
                movie.cloud_bucket,
                movie.cloud_file_path,
                temp_file
            )
            cls.save_movie_fingerprints(movie, temp_file)
            return True
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
