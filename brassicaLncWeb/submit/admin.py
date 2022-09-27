"""LncRna project admin panel config for submit app"""
from django.contrib import admin
from .models import SubmitedData

# Register your models here.
admin.site.register(SubmitedData)
