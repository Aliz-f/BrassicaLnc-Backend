from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination

from lncRNA.serializer import lncSerializer
from lncRNA.models import lnc


# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

# Create your views here.
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
