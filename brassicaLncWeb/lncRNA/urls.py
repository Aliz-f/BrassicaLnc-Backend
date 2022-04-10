from django.urls import path
from .views import *

urlpatterns = [
    path('create/lnc/', createLNC.as_view(), name='createLNC'),
    path('create/gtf/', createGTF.as_view(), name='createGTF'),
    path('transcripts/', transcripts.as_view(), name='transcripts'),
    path("chemical/",chemical.as_view(),name="chemical"),
    path("create/chemicaldb/",create_chemical_db.as_view(),name="createChemical"),
    path("transcript/each/", eachTranscript.as_view(), name='eachTranscript'),
]
