from django.urls import path
from .views import *

urlpatterns = [
    path('csv/', downloadCSV.as_view(), name = 'download-csv'),
    path('txt/', downloadTXT.as_view(), name = 'download-txt'),
    path('fasta/', downloadFASTA.as_view(), name = 'download-fasta'),
    path('gtf/', downloadGTF.as_view(), name = 'download-gtf'),

]
