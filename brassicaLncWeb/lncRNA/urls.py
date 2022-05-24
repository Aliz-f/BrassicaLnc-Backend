from django.urls import path
from .views import *

urlpatterns = [
    path('create/lnc/', createLNC.as_view(), name='createLNC'),
    path('create/gtf/', createGTF.as_view(), name='createGTF'),
    path('transcripts/', transcripts.as_view(), name='transcripts'),
    path("chemical/",chemical.as_view(),name="chemical"),
    path("abiotic/",abiotic.as_view(),name="Abiotic"),
    path("genetics/",genetics.as_view(),name="genetics"),
    path("developmental/",abiotic.as_view(),name="developmental"),
    path("biotic/",biotic.as_view(),name="biotic"),

    path("create/chemicaldb/",create_chemical_db.as_view(),name="createChemical"),
    path("create/abioticdb/",create_abiotic_db.as_view(),name="createAbiotic"),
    path("create/geneticsdb/",create_genetics_db.as_view(),name="createGenetics"),
    path("create/developmentaldb/",create_developmental_db.as_view(),name="createDevelopmental"),
    path("create/bioticdb/",create_biotic_db.as_view(),name="createBiotic"),

    # path("statistics/",statistics.as_view(),name="Statistics"),

    path("transcript/each/", eachTranscript.as_view(), name='eachTranscript'),
]
