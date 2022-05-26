from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination

from .serializer import * 
from .models import *

# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

class plotStatistic(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)
    
    def get(self, request):
        try:
            relationship=relationshipBetween_Chr_Gene_LncRNA.objects.all()
            filtrationSteps=filtrationStepsLncRNAIdentificationPipeline.objects.all()
            subdivisionLncRNAs=subdivisionLncRNAsAccordingClassCodes.objects.all()
            relationshipSer = relationshipBetween_Chr_Gene_LncRNASerializer(relationship, many=True)
            filtrationStepsSer=filtrationStepsLncRNAIdentificationPipelineSerializer(filtrationSteps, many=True)
            subdivisionLncRNAsSer=relationshipBetween_Chr_Gene_LncRNASerializer(subdivisionLncRNAs, many=True)
            data = {}
            data['relationship'] = relationshipSer.data
            data['filtrationSteps'] = filtrationStepsSer.data
            data['subdivisionLncRNAs'] = subdivisionLncRNAsSer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)