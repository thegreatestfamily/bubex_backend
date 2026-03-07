import cv2
import numpy as np
import os
from django.conf import settings
from .models import VideoFingerprint

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
        
        # In a real scenario, we might want to batch these or use a more efficient storage
        # For now, we store them as a JSON list in a single VideoFingerprint entry per movie segment
        # Or better, one entry per 15-30 second segment.
        
        # For simplicity, we'll store all fingerprints for this movie in one entry
        # (Though in production you'd use a vector DB or specialized hash index)
        VideoFingerprint.objects.create(
            movie=movie,
            fingerprint_data={'hashes': fingerprints},
            start_time_offset=0,
            duration=len(fingerprints) # roughly
        )
