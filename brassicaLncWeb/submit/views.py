from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

from .models import submittedData
from .serializer import submittedDataSerializer
from .utils import sendEmail
# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

class submitRecord(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)
    
    def post(self, request):
        try:
            data = request.data
            ser = submittedDataSerializer(data=data, partial=True)
            if ser.is_valid():
                ser.save()
                emailStatus = sendEmail(ser.data)
                if emailStatus:
                    return Response({"data":ser.data, 'email':True}, status.HTTP_201_CREATED)
                else:
                    return Response({"data":ser.data, 'email':False}, status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({'details':str(e)}, status=status.HTTP_400_BAD_REQUEST)