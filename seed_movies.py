import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bubex_core.settings')
django.setup()

from movie_database.models import Movie
from video_fingerprinting.services import FingerprintService

def seed_data():
    # Sample movie 1: The Matrix
    movie1, created = Movie.objects.get_or_create(
        title="The Matrix",
        director="The Wachowskis",
        composer="Don Davis",
        release_year=1999,
        genre="Sci-Fi",
        description="A computer hacker learns from mysterious rebels about the true nature of his reality.",
        poster_url="https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTYxZTM3ZGJiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        duration_minutes=136
    )
    
    # Normally we'd process a real file here
    # FingerprintService.save_movie_fingerprints(movie1, "path/to/matrix.mp4")
    
    # For testing without a real file, we'll manually create some dummy fingerprints
    from video_fingerprinting.models import VideoFingerprint
    if not VideoFingerprint.objects.filter(movie=movie1).exists():
        VideoFingerprint.objects.create(
            movie=movie1,
            fingerprint_data={'hashes': [{'timestamp': 0.0, 'hash': 'f0f0f0f0f0f0f0f0'}]},
            start_time_offset=0,
            duration=120
        )
    
    print("Seeded database with sample movie: The Matrix")

if __name__ == "__main__":
    seed_data()
