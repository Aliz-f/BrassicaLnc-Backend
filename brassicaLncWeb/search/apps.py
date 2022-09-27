"""django app config"""
from django.apps import AppConfig


class SearchConfig(AppConfig):
    """brassicaLncWeb.search app name"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
