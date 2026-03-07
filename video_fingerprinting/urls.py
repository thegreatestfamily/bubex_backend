from django.urls import path
from .views import ScanVideoView

urlpatterns = [
    path('', ScanVideoView.as_view(), name='scan_video'),
]
