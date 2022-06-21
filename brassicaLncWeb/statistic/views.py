from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination

from .serializer import * 
from .models import *
from collections import OrderedDict

# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


def ordered(d, desired_key_order):
    return OrderedDict([(key, d[key]) for key in desired_key_order])

toplevel_desired_key_order = ("Potential novel transripts (Class codes: i, u, x, o, e)", "Transcripts with length > 200 bp and < 15 kb", "Transcripts with FPKM > 0.5 in at least 495 samples","Transcripts after filter out tRNAs and rRNAs", "Noncoding transcripts predicted by CPC2", "LncRNAs predicted by PLncPRO, FEElnc, and CREMA", "Transcripts with no significant hit against UniProt, Pfam, and Rfam.", "Reliably expressed lncRNAs")
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
            filtrationStepsSer.data[0]['data'] =ordered(filtrationStepsSer.data[0]['data'], toplevel_desired_key_order)
            data['filtrationSteps'] = filtrationStepsSer.data
            data['subdivisionLncRNAs'] = subdivisionLncRNAsSer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)