from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination

from .serializer import lncSerializer, gtfSerializer
from .models import lnc


# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

class createLNC(APIView):
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

class createGTF(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)
    
    def post(self, request):
        try:
            print(request.data)
            ser = gtfSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class transcripts(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def get(self, request):
        try:
            geneId = request.GET.get('gid', None)
            transcriptId = request.GET.get('tid', None)
            chr = request.GET.get('chr', None)
            location = request.GET.get('loc', None)
            classification = request.GET.get('class', None)
            length = request.GET.get('len', None)
            exonNumber = request.GET.get('exon', None)
            page_size = request.GET.get('show', None)
            if not page_size:
                page_size=10
            page_size = int(page_size)
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            lncQuery = lnc.objects.all()
            if not geneId and not transcriptId and not chr and not location and not classification and not length and not exonNumber:
                result_page = paginator.paginate_queryset(list(lncQuery), request)
            else:
                if geneId :
                    lncQuery = lncQuery.filter(geneId=geneId)
                if transcriptId:
                    lncQuery = lncQuery.filter(transcriptId=transcriptId)
                if chr:
                    lncQuery = lncQuery.filter(chr=chr)
                if location:
                    location = location.split(',')
                    lncQuery = lncQuery.filter(locStart__gt=location[0])
                    lncQuery = lncQuery.filter(locEnd__lt=location[1])
                if classification:
                    lncQuery = lncQuery.filter(classification=classification)
                if length:
                    length = length.split(',')
                    lncQuery = lncQuery.filter(length__range=length)
                if exonNumber:
                    exonNumber = exonNumber.split(',')
                    lncQuery = lncQuery.filter(exonNumber__range=exonNumber)
                
                result_page = paginator.paginate_queryset(list(lncQuery), request)

            ser = lncSerializer(result_page, many=True)
            data = {"data": ser.data, 'pages': int(lncQuery.count()/page_size)+1}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)        