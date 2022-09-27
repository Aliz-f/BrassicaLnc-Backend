"""LncRna project serializer for lncRNA app"""

from rest_framework.exceptions import APIException
from rest_framework import serializers, status

from django.utils.encoding import force_str

from .models import (Lnc, Gtf, ChemicalFpkm,
    AbioticFpkm, GeneticsFpkm, DevelopmentalFpkm,
    BioticFpkm, Transposon, SmallRnaTarget, PremiRna, Etms,
    TargetDowngene, DowngeneDescription
)

class CustomValidation(APIException):
    """Custom validation for serializers """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {'detail': force_str(self.default_detail)}

class LncSerializer(serializers.ModelSerializer):
    """Serializer for Lnc model"""
    class Meta:
        """no docstring"""
        model = Lnc
        fields = "__all__"

class GtfSerializer(serializers.ModelSerializer):
    """Serializer for Gtf model"""
    class Meta:
        """no docstring"""
        model= Gtf
        fields = "__all__"

class ChemicalSerializer(serializers.ModelSerializer):
    """Serializer for ChemicalFpkm model"""
    class Meta:
        """no docstring"""
        model=ChemicalFpkm
        fields = "__all__"

class AbioticSerializer(serializers.ModelSerializer):
    """Serializer for AbioticFpkm model"""
    class Meta:
        """no docstring"""
        model=AbioticFpkm
        fields = "__all__"

class GeneticsSerializer(serializers.ModelSerializer):
    """Serializer for GeneticsFpkm model"""
    class Meta:
        """no docstring"""
        model=GeneticsFpkm
        fields = "__all__"

class DevelopmentalSerializer(serializers.ModelSerializer):
    """Serializer for DevelopmentalFpkm model"""
    class Meta:
        """no docstring"""
        model=DevelopmentalFpkm
        fields = "__all__"

class BioticSerializer(serializers.ModelSerializer):
    """Serializer for BioticFpkm model"""
    class Meta:
        """no docstring"""
        model=BioticFpkm
        fields = "__all__"

class TransposonSerializer(serializers.ModelSerializer):
    """Serializer for Transposon model"""
    class Meta:
        """no docstring"""
        model=Transposon
        fields = "__all__"

class SmallRnaTargetSerializer(serializers.ModelSerializer):
    """Serializer for SmallRnaTarget model"""
    class Meta:
        """no docstring"""
        model=SmallRnaTarget
        fields = "__all__"

class PremiRnaSerializer(serializers.ModelSerializer):
    """Serializer for PremiRna model"""
    class Meta:
        """no docstring"""
        model=PremiRna
        fields = "__all__"

class EtmsSerializer(serializers.ModelSerializer):
    """Serializer for Etms model"""
    class Meta:
        """no docstring"""
        model = Etms
        fields = "__all__"

class TargetDowngeneSerializer(serializers.ModelSerializer):
    """Serializer for TargetDowngene model"""
    class Meta:
        """no docstring"""
        model = TargetDowngene
        fields = "__all__"

class DowngeneDescriptionSerializer(serializers.ModelSerializer):
    """Serializer for DowngeneDescription model"""
    class Meta:
        """no docstring"""
        model = DowngeneDescription
        fields = "__all__"
