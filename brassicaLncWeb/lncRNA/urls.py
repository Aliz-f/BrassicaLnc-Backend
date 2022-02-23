from django.urls import path
from .views import createDatabase

urlpatterns = [
    path('set/', createDatabase.as_view(), name='createDatabase'),
]
