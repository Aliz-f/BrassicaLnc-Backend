"""LncRna project views for submit app"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

from .models import SubmitedData
from .serializer import SubmitedDataSerializer
from .utils import send_email

class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """CsrfExempt Session Authentication"""
    def enforce_csrf(self, request):
        return

class SubmitRecord(APIView):
    """
    Api for submitting a new record
    data format:
        {
            "email":"",
            "chromosome":"",
            "location":"",
            "strand":"",
            "exonLocation":"",
            "sequence":"",
            "name":"",
            "expressionValue":"",
            "sampleInformation":"",
            "experimentalDesign":"",
            "lncRNAFunction":"",
            "reference":"",
            "otherInformation":""
        }

    test1 : {
            "email":"fad127alireza2@gmail.com",
            "chromosome":"Mt",
            "location":"1101-4206",
            "strand":"+",
            "exonLocation":"96343222,96348289,96349707,96358894",
            "sequence":"TCTAGAACCCTAGCGGGCGGCGAGGAC",
            "name":"Osa01LNT0000100.1",
            "expressionValue":"0.76",
            "sampleInformation":"intergenetic lncRNA (lincRNA)",
            "experimentalDesign":"",
            "lncRNAFunction":"",
            "reference":"",
            "otherInformation":""
        }
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def post(self, request) -> Response:
        """no docstring"""
        try:
            data = request.data
            ser = SubmitedDataSerializer(data=data, partial=True)
            if ser.is_valid():
                ser.save()
                email_status = send_email(ser.data)
                if email_status:
                    return Response({"data":ser.data, 'email':True}, status.HTTP_201_CREATED)
                return Response({"data":ser.data, 'email':False}, status.HTTP_201_CREATED)
            return Response(ser.errors, status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as error:
            return Response({'details':str(error)}, status=status.HTTP_400_BAD_REQUEST)
