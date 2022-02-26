from django.urls import path
from .views import *

urlpatterns = [
    path('csv/', downloadCSV.as_view(), name = 'download-csv'),
    path('txt/', downloadTXT.as_view(), name = 'download-txt'),
]
