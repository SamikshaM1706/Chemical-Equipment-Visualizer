from django.contrib import admin
from django.urls import path
from api.views import upload_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', upload_csv),
]
