import os

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
                return Response({'detail': 'query params not found'}, status=status.HTTP_400_BAD_REQUEST)
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

    def post(self, request):
        try:
            page_size = 6
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            data = request.data
            
            geneId = data.get('geneId', None)
            # assert geneId, 'geneId not found'
            transcript = data.get('tranId', None)
            assert transcript or geneId, 'transcript and geneId not found'
            if geneId:
                lncQuery = lnc.objects.filter(geneId=geneId)
                assert lncQuery, 'query not found'
            elif transcript:
                lncQuery = lnc.objects.filter(transcriptId=transcript)
                assert lncQuery, 'query not found'
            
            result_page = paginator.paginate_queryset(lncQuery, request)
            ser = lncSerializer(result_page, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class searchByExp(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def get(self, request):
        try:
            page_size = 10
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            """
                group list allow : chemical,
            """
            group = request.GET.get('group', None)
            assert group, 'group key not found'
            startRange = request.GET.get('startRange', None)
            endRange = request.GET.get('endRange', None)
            filePath = os.getcwd() + f'/download/files/{group}/{group}_fpkm.txt'
            list=[]
            transcripts = []
            with open(filePath, 'r') as f:
                iter =0
                for line in f.readlines():
                    if iter!=0:
                        list.append(line.split('\t'))
                    iter+=1

                for i in range(1,len(list)):
                    for j in range(1,len(list[i])):
                        list[i][j] = float(list[i][j]) 
                                
                for i in range(1,len(list)):
                    for j in range(len(list[i])):
                        if j!=0:
                            if float(startRange)<list[i][j]<float(endRange):
                                flag = True
                            else:
                                flag=False
                                break
                    if flag:
                        transcripts.append(list[i][0])
            lncQuery = lnc.objects.filter(transcriptId__in=transcripts)
            result_page = paginator.paginate_queryset(lncQuery, request)
            ser = lncSerializer(result_page, many=True)
            data = {"data": ser.data, 'pages': int(lncQuery.count()/page_size)+1,"group":group}
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"details":str(e)}, status=status.HTTP_400_BAD_REQUEST)