from django.urls import path
from .views import *

urlpatterns = [
    path('', submitRecord.as_view(), name='submit-records'),
]
