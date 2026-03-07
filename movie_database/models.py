from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    composer = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=100)
    poster_url = models.URLField(max_length=500, null=True, blank=True)
    trailer_url = models.URLField(max_length=500, null=True, blank=True)
    imdb_id = models.CharField(max_length=20, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    # Cloud Storage Fields
    cloud_bucket = models.CharField(max_length=255, null=True, blank=True)
    cloud_file_path = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
