from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination

from .serializer import lncSerializer
from .models import lnc

# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

class createDatabase(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)
    
    def post(self, request):
        try:
            ser = lncSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:
            page_size = int(request.GET.get('show', None))
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            lncQuery = lnc.objects.all()
            result_page = paginator.paginate_queryset(list(lncQuery), request)
            ser = lncSerializer(result_page, many=True)
            data = {"data": ser.data, 'pages': int(lncQuery.count()/page_size)+1}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class searchById(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def post(self, request):
        try:
            page_size = 6
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            data = request.data
            
            geneId = data.get('geneId', None)
            assert geneId, 'geneId not found'

            lncQuery = lnc.objects.filter(geneId=geneId)
            assert lncQuery, 'query not found'

            result_page = paginator.paginate_queryset(lncQuery, request)
            ser = lncSerializer(result_page, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        