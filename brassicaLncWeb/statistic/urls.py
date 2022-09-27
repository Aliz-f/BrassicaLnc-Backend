"""LncRna project urls for statistic app"""
from django.urls import path
from .views import StatisticPlot

urlpatterns = [
    path('', StatisticPlot.as_view(), name='statistic'),
]
