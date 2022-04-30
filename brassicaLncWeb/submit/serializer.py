from rest_framework.exceptions import APIException
from rest_framework import serializers, status
from django.utils.encoding import force_str
from .models import submittedData

class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None: self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {'detail': force_str(self.default_detail)}


class submittedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = submittedData
        fields = "__all__"


    def create(self, validated_data):
        try:
            needed_keys = ["email", 'chromosome', 'location', 'strand', 'exonLocation', 'sequence']
            flag = False
            for value in validated_data:
                if all(key in validated_data for key in needed_keys):
                    flag=True
            if flag:
                return submittedData.objects.create(**validated_data)
            else:
                return CustomValidation('error in items', 'detail', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return str(e)
    # def create(self, validated_data):
    #     return submitedData.objects.create(**validated_data)