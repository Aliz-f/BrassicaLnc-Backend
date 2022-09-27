"""LncRna project views for search app"""
import os
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination
from lncRNA.serializer import LncSerializer
from lncRNA.models import Lnc

class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """CsrfExempt Session Authentication"""
    def enforce_csrf(self, request):
        return

class SearchById(APIView):
    """
    Api for search lnc data
    - default data per page=10
    Query params:
        - search=BnaCnnLNG0016000,BnaCnnLNG0016000.1
        - chr=chrUnn_random
        - loc=6828472,6829748
        - class=u
        - len=100,10000
        - exon=0,2
        - show=20
        - page=10
        - NONE (return all data with pagination)

        test1 : ?loc=68,6829800&exon=0,2&chr=chrUnn_random&class=u&len=10,1000
        test2 : ?search=BnaCnnLNG0016000,BnaCnnLNG0016000.1
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self, request) -> Response:
        """no docstring"""
        try:
            search_box = request.GET.get('search', None)
            lnc_chr = request.GET.get('chr', None)
            location = request.GET.get('loc', None)
            classification = request.GET.get('class', None)
            length = request.GET.get('len', None)
            exon_number = request.GET.get('exon', None)
            page_size = request.GET.get('show', 10)
            page_size = int(page_size)
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            query = Q()
            if search_box:
                search_box = search_box.split(',')
                for each_query in search_box:
                    each_query = each_query.replace(' ', '')
                    if '.' in each_query:
                        query &= Q(transcriptId = each_query)
                    else:
                        query &= Q(geneId = each_query)
            if lnc_chr:
                query &=Q(chr = lnc_chr)
            if location:
                location = location.split(',')
                query &= Q(locStart__gt=location[0]) & Q(locEnd__lt=location[1])
            if classification:
                query &= Q(classification=classification)
            if length:
                length = length.split(',')
                query &= Q(length__range=length)
            if exon_number:
                exon_number = exon_number.split(',')
                query &= Q(exonNumber__range=exon_number)

            lnc_query = Lnc.objects.filter(query).order_by('id')
            result_page = paginator.paginate_queryset(lnc_query, request)
            pages = lnc_query.count()/page_size if \
                isinstance(int, type(lnc_query.count()/page_size)) else \
                int(lnc_query.count()/page_size)+1
            ser = LncSerializer(result_page, many=True)
            data = {"data": ser.data, 'pages': pages, "count": lnc_query.count()}
            return Response(data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request) -> Response:
        """Get transcripts with filter with post method"""
        try:
            page_size = 6
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            data = request.data

            gene_id = data.get('geneId', None)
            # assert gene_id, 'gene_id not found'
            transcript = data.get('tranId', None)
            assert transcript or gene_id, 'transcript and gene_id not found'
            if gene_id:
                lnc_query = Lnc.objects.filter(geneId=gene_id)
                assert lnc_query, 'query not found'
            elif transcript:
                lnc_query = Lnc.objects.filter(transcriptId=transcript)
                assert lnc_query, 'query not found'

            result_page = paginator.paginate_queryset(lnc_query, request)
            ser = LncSerializer(result_page, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)

class SearchByExp(APIView):
    """
    Api for search by Expressions
    Query params:
        - group = ( genetics | abiotic | biotic | developmental | chemical)
        - startRange = 12
        - endRange = 20

        test1 : ?group=chemical&startRange=10&endRange=2000
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self, request) -> Response:
        """no docstring"""
        try:
            page_size = int(request.GET.get('per_page', 10))
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            group = request.GET.get('group', None)
            assert group, 'group key not found'
            start_range = request.GET.get('startRange', None)
            end_range = request.GET.get('endRange', None)
            file_path = os.getcwd() + f'/files/{group}/v2/{group}_fpkm.txt'
            group_list=[]
            transcripts = []
            flag=False
            with open(file_path, 'r') as file_handeler:
                iterator =0
                for line in file_handeler.readlines():
                    if iterator!=0:
                        temp=line.split('\t')
                        if len(temp)==1:
                            group_list.append(temp[0].split(' '))
                        else:
                            group_list.append(temp)
                    iterator+=1

                for i in range(len(group_list)):
                    for j in range(1, len(group_list[i])):
                        group_list[i][j] = float(group_list[i][j])              
                for i in range(len(group_list)):
                    for j in range(len(group_list[i])):
                        if j!=0:
                            if float(start_range)<=group_list[i][j]<=float(end_range):
                                flag = True
                            else:
                                flag=False
                                break
                    if flag:
                        transcripts.append(group_list[i][0])
            lnc_query = Lnc.objects.filter(transcriptId__in=transcripts)
            result_page = paginator.paginate_queryset(lnc_query, request)
            ser = LncSerializer(result_page, many=True)
            pages = lnc_query.count()/page_size if \
                isinstance(int, type(lnc_query.count()/page_size)) else \
                int(lnc_query.count()/page_size)+1
            data = dict(
                data = ser.data,
                pages = pages,
                count = lnc_query.count(),
                group = group
            )
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"details":str(error)}, status=status.HTTP_400_BAD_REQUEST)
