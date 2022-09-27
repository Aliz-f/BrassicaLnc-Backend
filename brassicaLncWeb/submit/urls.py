"""LncRna project urls for submit app"""
from django.urls import path
from .views import SubmitRecord

urlpatterns = [
    path('', SubmitRecord.as_view(), name='submit-records'),
]
