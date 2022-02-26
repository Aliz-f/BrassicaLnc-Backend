from django.urls import path
from .views import *

urlpatterns = [
    path('create/', createDatabase.as_view(), name='createDatabase'),
    path('transcripts/', transcripts.as_view(), name='transcripts'),
]
