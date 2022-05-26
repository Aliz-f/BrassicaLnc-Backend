from django.urls import path
from .views import *

urlpatterns = [
    path('', plotStatistic.as_view(), name='statistic'),
]