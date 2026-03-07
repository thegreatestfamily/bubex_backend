from django.db import models
from movie_database.models import Movie

class VideoFingerprint(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='fingerprints')
    # The fingerprint itself can be stored as a binary blob or a JSON field
    # For simplicity in this implementation, we'll store it as a JSON field
    fingerprint_data = models.JSONField()
    start_time_offset = models.FloatField(help_text="Start time in seconds within the movie")
    duration = models.FloatField(help_text="Duration of this fingerprint segment")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fingerprint for {self.movie.title} at {self.start_time_offset}s"
