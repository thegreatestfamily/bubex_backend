from django.core.management.base import BaseCommand
from movie_database.models import Movie
from video_fingerprinting.services import FingerprintService

class Command(BaseCommand):
    help = 'Syncs movies from Google Cloud Storage and generates fingerprints'

    def handle(self, *args, **options):
        movies = Movie.objects.exclude(cloud_file_path__isnull=True).exclude(cloud_file_path__exact='')
        
        self.stdout.write(self.style.SUCCESS(f'Found {movies.count()} cloud-linked movies.'))
        
        for movie in movies:
            self.stdout.write(f'Processing: {movie.title}...')
            success = FingerprintService.process_cloud_movie(movie)
            if success:
                self.stdout.write(self.style.SUCCESS(f'Successfully fingerprinted {movie.title}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to process {movie.title}'))
