from django.urls import path
from .views import ScanVideoView, SyncCloudMoviesView

urlpatterns = [
    path('scan/', ScanVideoView.as_view(), name='scan-video'),
    path('sync-cloud/', SyncCloudMoviesView.as_view(), name='sync-cloud'),
]
