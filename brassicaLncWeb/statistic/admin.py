"""LncRna project admin panel config for statistic app"""
from django.contrib import admin
from .models import (RelationshipBetweenChrGeneLncRna,
    FiltrationStepsLncRnaIdentificationPipeline,
    SubdivisionLncRnasAccordingClassCodes
)

admin.site.register(
    [
        RelationshipBetweenChrGeneLncRna,
        FiltrationStepsLncRnaIdentificationPipeline,
        SubdivisionLncRnasAccordingClassCodes
    ]
)
