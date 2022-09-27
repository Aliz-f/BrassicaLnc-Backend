"""LncRna project urls for download app"""
from django.urls import path
from .views import (DownloadAllFiles, LncDownloadCsvFormat,
        LncDownloadTxtFormat, LncDownloadFastaFormat,
        LncDownloadGtfFormat, GroupDownloadCsvFpkm,
        DownloadStructurePremiRna)

urlpatterns = [
    path('', DownloadAllFiles.as_view(), name = 'download_all_files'),
    path('csv/', LncDownloadCsvFormat.as_view(), name = 'download_csv_format'),
    path('txt/', LncDownloadTxtFormat.as_view(), name = 'download_txt_format'),
    path('fasta/', LncDownloadFastaFormat.as_view(), name = 'download_fasta_format'),
    path('gtf/', LncDownloadGtfFormat.as_view(), name = 'download_gtf_format'),
    path('fpkm/csv/', GroupDownloadCsvFpkm.as_view(), name = 'download_csv_fpkm'),
    path("premi_rna/structure/",
            DownloadStructurePremiRna.as_view(),name="download_premiRNA_structure"),
]
