from rest_framework.exceptions import APIException
from rest_framework import serializers, status

from django.utils.encoding import force_str

from .models import lnc, gtf,chemicalFpkm, abioticFpkm, geneticsFpkm

class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None: self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {'detail': force_str(self.default_detail)}

class lncSerializer(serializers.ModelSerializer):
    class Meta:
        model = lnc
        fields = "__all__"

    def create(self, validated_data):
        return lnc.objects.create(**validated_data)

class gtfSerializer(serializers.ModelSerializer):
    class Meta:
        model= gtf
        fields = "__all__"

    def create(self, validated_data):
        return gtf.objects.create(**validated_data)

class chemicalSerializer(serializers.ModelSerializer):
    class Meta:
        model=chemicalFpkm
        fields = "__all__"

class abioticSerializer(serializers.ModelSerializer):
    class Meta:
        model=abioticFpkm
        fields = "__all__"


class geneticsSerializer(serializers.ModelSerializer):
    class Meta:
        model=geneticsFpkm
        fields = "__all__"