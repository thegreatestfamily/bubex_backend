import os
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .serializers import ScanResponseSerializer
from matching_engine.services import MatchingService
from movie_database.serializers import MovieSerializer

class ScanVideoView(APIView):
    # For now, allow anybody to scan (IsAuthenticatedOrReadOnly is default)
    permission_classes = [] 

    def post(self, request, *args, **kwargs):
        if 'video' not in request.FILES:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        video_file = request.FILES['video']
        start_time = time.time()
        
        # Save temporary video file
        path = default_storage.save('tmp/scans/' + video_file.name, ContentFile(video_file.read()))
        full_path = default_storage.path(path)
        
        try:
            # Find the best match
            match = MatchingService.find_match(full_path)
            processing_time = time.time() - start_time
            
            if match and match['movie']:
                movie_data = MovieSerializer(match['movie']).data
                response_data = {
                    'success': True,
                    'movie': movie_data,
                    'confidence': match['confidence'],
                    'message': 'Match found!',
                    'processing_time': processing_time
                }
            else:
                response_data = {
                    'success': False,
                    'movie': None,
                    'confidence': 0.0,
                    'message': 'No movie found. Try another scene!',
                    'processing_time': processing_time
                }
            
            serializer = ScanResponseSerializer(response_data)
            return Response(serializer.data)
            
        finally:
            # Clean up temporary file
            if os.path.exists(full_path):
                os.remove(full_path)

class SyncCloudMoviesView(APIView):
    """
    Endpoint to trigger fingerprinting of movies hosted on GCS.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        from movie_database.models import Movie
        from .services import FingerprintService
        
        movies = Movie.objects.exclude(cloud_file_path__isnull=True).exclude(cloud_file_path__exact='')
        results = []
        
        for movie in movies:
            success = FingerprintService.process_cloud_movie(movie)
            results.append({
                'movie': movie.title,
                'status': 'success' if success else 'failed'
            })
            
        return Response({
            'message': f'Processed {len(results)} movies',
            'details': results
        }, status=status.HTTP_200_OK)
