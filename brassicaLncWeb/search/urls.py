from django.urls import path
from .views import *

urlpatterns = [
    path('id/', searchById.as_view(), name = 'search-by-id' ),
    path('exp/', searchByExp.as_view(), name = 'search-by-exp'),
]
