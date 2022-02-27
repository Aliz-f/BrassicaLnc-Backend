from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions


from lncRNA.models import lnc
from .utils import exportCSV, exportTXT, exportFasta


# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

# Create your views here.
class downloadCSV(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def get(self, request):
        try:
            idList = request.GET.get('ids', None)
            lncList = []
            if idList == None:
                lncQuery = lnc.objects.all()
                return exportCSV(list(lncQuery))
            else:
                idList = idList.split(',')
                lncQuery = lnc.objects.filter(id__in=idList)
                return exportCSV(list(lncQuery))
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class downloadTXT(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def get(self, request):
        try:
            idList = request.GET.get('ids', None)
            lncList = []
            if idList == None:
                lncQuery = lnc.objects.all()
                return exportTXT(list(lncQuery))
            else:
                idList = idList.split(',')
                lncQuery = lnc.objects.filter(id__in=idList)
                return exportTXT(list(lncQuery))
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class downloadFASTA(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def get(self, request):
        try:
            idList = request.GET.get('ids', None)
            lncList = []
            if idList == None:
                lncQuery = lnc.objects.all()
                return exportFasta(list(lncQuery))
            else:
                idList = idList.split(',')
                lncQuery = lnc.objects.filter(id__in=idList)
                return exportFasta(list(lncQuery))
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class downloadGTF(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def get(self, request):
        try:
            idList = request.GET.get('ids', None)
            lncList = []
            if idList == None:
                lncQuery = lnc.objects.all()
                return exportFasta(list(lncQuery))
            else:
                idList = idList.split(',')
                lncQuery = lnc.objects.filter(id__in=idList)
                return exportFasta(list(lncQuery))
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
