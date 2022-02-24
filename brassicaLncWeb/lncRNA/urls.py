from django.urls import path
from .views import *

urlpatterns = [
    path('set/', createDatabase.as_view(), name='createDatabase'),
    path('search/id/', searchById.as_view(), name = 'search-by-id' ),

]
