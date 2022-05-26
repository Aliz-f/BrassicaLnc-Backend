from rest_framework.exceptions import APIException
from rest_framework import serializers, status

from django.utils.encoding import force_str

from .models import *

class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None: self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {'detail': force_str(self.default_detail)}

class relationshipBetween_Chr_Gene_LncRNASerializer(serializers.ModelSerializer):
    class Meta:
        model=relationshipBetween_Chr_Gene_LncRNA
        fields = "__all__"

class filtrationStepsLncRNAIdentificationPipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model=filtrationStepsLncRNAIdentificationPipeline
        fields = "__all__"

class subdivisionLncRNAsAccordingClassCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model=subdivisionLncRNAsAccordingClassCodes
        fields = "__all__"