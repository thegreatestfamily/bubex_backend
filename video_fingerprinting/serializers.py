from rest_framework import serializers
from movie_database.serializers import MovieSerializer

class ScanResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    movie = MovieSerializer(required=False)
    confidence = serializers.FloatField()
    message = serializers.CharField()
    processing_time = serializers.FloatField()
