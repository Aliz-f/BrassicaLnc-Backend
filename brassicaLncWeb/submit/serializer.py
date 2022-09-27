"""LncRna project serializer for submit app"""
from rest_framework.exceptions import APIException
from rest_framework import serializers, status
from django.utils.encoding import force_str
from .models import SubmitedData

class CustomValidation(APIException):
    """Custom validation"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {'detail': force_str(self.default_detail)}


class SubmitedDataSerializer(serializers.ModelSerializer):
    """serializer for submited data"""
    class Meta:
        """no docstring"""
        model = SubmitedData
        fields = "__all__"


    def create(self, validated_data):
        try:
            needed_keys = ["email", 'chromosome', 'location', 'strand', 'sequence']
            flag = False
            for value in validated_data:
                if all(key in validated_data for key in needed_keys):
                    flag=True
            if flag:
                return SubmitedData.objects.create(**validated_data)
            return CustomValidation(
                'error in items',
                'detail',
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as error:
            return str(error)
