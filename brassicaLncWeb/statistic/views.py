"""LncRna project views for statistic app"""
from collections import OrderedDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

from .serializer import (
    RelationshipBetweenChrGeneLncRnaSerializer,
    FiltrationStepsLncRnaIdentificationPipelineSerializer,
    SubdivisionLncRnasAccordingClassCodesSerializer,
)
from .models import (
    RelationshipBetweenChrGeneLncRna,
    FiltrationStepsLncRnaIdentificationPipeline,
    SubdivisionLncRnasAccordingClassCodes
)

# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """CsrfExempt Session Authentication"""
    def enforce_csrf(self, request):
        return


def ordered(data, desired_key_order)-> OrderedDict:
    """no docstring"""
    return OrderedDict([(key, data[key]) for key in desired_key_order])

toplevel_desired_key_order = (
    "Potential novel transripts (Class codes: i, u, x, o, e)",
    "Transcripts with length > 200 bp and < 15 kb",
    "Transcripts with FPKM > 0.5 in at least 495 samples",
    "Transcripts after filter out tRNAs and rRNAs",
    "Noncoding transcripts predicted by CPC2",
    "LncRNAs predicted by PLncPRO, FEElnc, and CREMA",
    "Transcripts with no significant hit against UniProt, Pfam, and Rfam.",
    "Reliably expressed lncRNAs"
)
class StatisticPlot(APIView):
    """Api for get statistic data for plots"""
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self, request) -> Response:
        """no docstring"""
        try:
            relationship=RelationshipBetweenChrGeneLncRna.objects.all()
            filtration_steps=FiltrationStepsLncRnaIdentificationPipeline.objects.all()
            subdivision_lnc_rnas=SubdivisionLncRnasAccordingClassCodes.objects.all()
            relationship_serializer = RelationshipBetweenChrGeneLncRnaSerializer(
                relationship, many=True
            )
            filtration_steps_serializer=FiltrationStepsLncRnaIdentificationPipelineSerializer(
                filtration_steps, many=True
            )
            subdivision_lnc_rnas_serializer=SubdivisionLncRnasAccordingClassCodesSerializer(
                subdivision_lnc_rnas, many=True
            )
            data = {}
            data['relationship'] = relationship_serializer.data
            filtration_steps_serializer.data[0]['data']= \
            ordered(filtration_steps_serializer.data[0]['data'], toplevel_desired_key_order)
            data['filtrationSteps'] = filtration_steps_serializer.data
            data['subdivisionLncRNAs'] = subdivision_lnc_rnas_serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'detail':str(error)}, status=status.HTTP_400_BAD_REQUEST)
