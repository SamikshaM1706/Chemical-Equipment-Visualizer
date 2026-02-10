from django.urls import path
from .views import UploadCSV

urlpatterns = [
    path('api/upload/', UploadCSV.as_view(), name='upload-csv'),
]
