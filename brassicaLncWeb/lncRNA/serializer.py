from rest_framework import serializers
from .models import lnc

class lncSerializer(serializers.ModelSerializer):
    class Meta:
        model = lnc
        fields = "__all__"

    def create(self, validated_data):
        return lnc.objects.create(**validated_data)