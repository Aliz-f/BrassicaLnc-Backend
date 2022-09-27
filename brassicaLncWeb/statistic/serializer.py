"""LncRna project serializer for statistic app"""

from rest_framework.exceptions import APIException
from rest_framework import serializers, status

from django.utils.encoding import force_str

from .models import (RelationshipBetweenChrGeneLncRna,
    FiltrationStepsLncRnaIdentificationPipeline,
    SubdivisionLncRnasAccordingClassCodes
)

class CustomValidation(APIException):
    """Custom validation for serializers"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {'detail': force_str(self.default_detail)}

class RelationshipBetweenChrGeneLncRnaSerializer(serializers.ModelSerializer):
    """serializer for RelationshipBetweenChrGeneLncRna"""
    class Meta:
        """no docstring"""
        model=RelationshipBetweenChrGeneLncRna
        fields = "__all__"

class FiltrationStepsLncRnaIdentificationPipelineSerializer(serializers.ModelSerializer):
    """serializer for FiltrationStepsLncRnaIdentificationPipeline"""
    class Meta:
        """no docstring"""
        model=FiltrationStepsLncRnaIdentificationPipeline
        fields = "__all__"

class SubdivisionLncRnasAccordingClassCodesSerializer(serializers.ModelSerializer):
    """serializer for SubdivisionLncRnasAccordingClassCodes"""
    class Meta:
        """no docstring"""
        model=SubdivisionLncRnasAccordingClassCodes
        fields = "__all__"
