"""LncRna project urls for search app"""
from django.urls import path
from .views import SearchById, SearchByExp

urlpatterns = [
    path('id/', SearchById.as_view(), name = 'search-by-id' ),
    path('exp/', SearchByExp.as_view(), name = 'search-by-exp'),
]
