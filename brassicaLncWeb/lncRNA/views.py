"""LncRna project views for lncRNA app"""
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from django.db.models import Q
from .serializer import (LncSerializer, GtfSerializer, SmallRnaTargetSerializer,
    PremiRnaSerializer, TransposonSerializer, ChemicalSerializer, DevelopmentalSerializer,
    GeneticsSerializer, AbioticSerializer, BioticSerializer, EtmsSerializer,
    TargetDowngeneSerializer, DowngeneDescriptionSerializer
)
from .models import (Lnc, Gtf, ChemicalFpkm, DevelopmentalFpkm,
    GeneticsFpkm, AbioticFpkm, BioticFpkm, Transposon, SmallRnaTarget,
    PremiRna, Etms, TargetDowngene, DowngeneDescription
)

class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """Csrf Exempt Session Authentication"""
    def enforce_csrf(self, request):
        return

class GetTranscripts(APIView):
    """
    Api for get all lnc data with filter
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
    parser_classes = (JSONParser,)
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
                lnc_chr = lnc_chr.replace(' ', '')
                query &=Q(chr = lnc_chr)
            if location:
                location = location.split(',')
                query &= Q(locStart__gt=location[0]) & Q(locEnd__lt=location[1])
            if classification:
                classification = classification.replace(' ', '')
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
            data = dict(
                data = ser.data,
                pages = pages,
                count = lnc_query.count()
            )
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(
                dict(detail = str(error)), status=status.HTTP_400_BAD_REQUEST
            )

class GetEachTranscript(APIView):
    """
    Api for get each transcript with other data such as:
    Gtf, SmallRna, PremiRna, etc...
    data format:
        {
            "tranId" : "BnaA01LNG0006800.1"
        }
        test1 : {"tranId" : "BnaA01LNG0006800.1"}
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def post(self, request) -> Response:
        """no docstring"""
        try:
            data = request.data
            transcript = data.get('tranId', None)
            assert transcript, 'tranId not found'
            lnc_query = Lnc.objects.get(transcriptId=transcript)
            gtf_query = Gtf.objects.filter(transcript_id=lnc_query.stringTieId)
            smallrna_query = SmallRnaTarget.objects.filter(lncrna_id=lnc_query.geneId)
            premirna_query = PremiRna.objects.filter(lncrna_id = lnc_query.geneId)
            transposon_query = Transposon.objects.filter(lncrna_id = lnc_query.geneId)

            lnc_serializer = LncSerializer(lnc_query)
            gtf_serializer = GtfSerializer(gtf_query,many=True)
            smallrna_serializer = SmallRnaTargetSerializer(smallrna_query, many=True)
            permirna_serializer = PremiRnaSerializer(premirna_query, many=True)
            transposon_serializer = TransposonSerializer(transposon_query, many=True)
            response = dict()
            response.update(
                dict(
                    lnc = lnc_serializer.data,
                    gtf = gtf_serializer.data,
                    smallRNA = smallrna_serializer.data,
                    premiRNA = permirna_serializer.data,
                    transposon = transposon_serializer.data
                )
            )
            return Response(response,status=status.HTTP_200_OK)
        except Exception as erorr:
            return Response(
                {'detail': str(erorr)}, status=status.HTTP_400_BAD_REQUEST
            )

class GetChemicalFpkm(APIView):
    """
    Get fpkm data for Chemical group
    data format:
        {
            "id": "BnaA01LNG0006800.1"
        }

        test1 : {"id": "BnaA01LNG0006800.1"}
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def post(self,request) -> Response:
        """no docstring"""
        try:
            data = list()
            dic = dict()
            desc = dict()
            file_path = os.getcwd() + '/files/chemical/v3/'
            with open(file_path + "Chemical_Table_v3.csv", 'r') as myfile:
                for line in myfile:
                    data.append(line.split(","))

                for i in data :
                    try:
                        try :
                            t= dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] 
                            t.append(i[1].split()[0].replace("&"," ").replace("$","-").replace("%",","))
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ]  = t
                        except Exception as e :
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] = [i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]
                            
                            
                    except Exception as e: 
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")]=dict()
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",")] =[i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]

                for i in data :
                    try:
                        try :
                            desc[i[4].split()[0]]  = i[5].split()[0].replace("&"," ").replace("$",",")
                        except Exception as e :
                    
                            desc[i[4].split()[0]]  = i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")           
                    except Exception as e: 
                        
                        desc[i[4].split()[0]] = dict() 
                        desc[i[4].split()[0]]  = i[5].split()[0].replace("&"," ").replace("$",",")
            id = request.data.get('id')
            transcript = ChemicalFpkm.objects.filter(lncRNAs__contains=id)
            a = dic
            responce = dict()
            for t in transcript :
                for i in dic.keys():
                    s=0
                    for j in dic[i].keys():
                        k = dic[i][j]
                        dat = ChemicalSerializer(t).data      
                        try:              
                            for z in k :
                                s += dat[z]
                            s/=len(k)
                            if round(s,4)==0:
                                 a[i][j]=round(s,8)
                            else:
                                a[i][j]=round(s,4)
                        except :
                            responce[dat["lncRNAs"]] = dic
                            #responce["desc"]=desc
                            return Response(responce)
                responce[dat["lncRNAs"]] = a 
                responce["desc"]=desc
            return Response(responce,status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetAbioticFpkm(APIView):
    """
    Get fpkm data for Abiotic group
    data format:
        {
            "id": "BnaA01LNG0006800.1"
        }

        test1 : {"id": "BnaA01LNG0006800.1"}
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )
    def post(self,request) -> Response:
        """no docstring"""
        try:
            data = []
            dic = dict()
            desc = dict()
            file_path = os.getcwd() + '/files/abiotic/v3/'
            with open(file_path + "Abiotic_Table_v3.csv", 'r') as myfile:
                for line in myfile:
                    data.append(line.split(","))

                for i in data :
                    try:
                        try :
                            t= dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] 
                            t.append(i[1].split()[0].replace("&"," ").replace("$","-").replace("%",","))
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ]  = t
                        except:
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] = [i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]
                    except: 
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")]=dict()
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",")] =[i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]

            for i in data :
                    try:
                        try :
                            desc[i[4].split()[0]]  = i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")
                        except:
                            desc[i[4].split()[0]] = i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")           
                    except: 
                        desc[i[4].split()[0]] = dict() 
                        desc[i[4].split()[0]]  = i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")         
            id = request.data["id"]
            transcript = AbioticFpkm.objects.filter(lncRNAs__contains=id)
            a = dic
            responce = dict()
            for t in transcript :
                for i in dic.keys():
                    s=0
                    for j in dic[i].keys():
                        k = dic[i][j]
                        dat = AbioticSerializer(t).data      
                        try:              
                            for z in k :
                                s += dat[z]
                            s/=len(k)
                            if round(s,4)==0:
                                 a[i][j]=round(s,8)
                            else:
                                a[i][j]=round(s,4)
                        except :
                            responce[dat["lncRNAs"]] = dic
                            return Response(responce)
                responce[dat["lncRNAs"]] = a 
                responce["desc"]=desc
            return Response(responce,status=status.HTTP_200_OK)
        except Exception as erorr:
            return Response(
                {'detail': str(erorr)}, status=status.HTTP_400_BAD_REQUEST
            )

class GetGeneticsFpkm(APIView):
    """
    Get fpkm data for Genetics group
    data format:
        {
            "id": "BnaA01LNG0006800.1"
        }

        test1 : {"id": "BnaA01LNG0006800.1"}
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )
    def post(self,request) -> Response:
        """no docstring"""
        try:
            data = []
            dic = dict()
            desc = dict()
            file_path = os.getcwd() + '/files/genetics/v3/'
            with open(file_path + "Genetics_Table_v3.csv", 'r') as myfile:
                for line in myfile:
                    data.append(line.split(","))

                for i in data :
                    try:
                        try :
                            t= dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] 
                            t.append(i[1].split()[0].replace("&"," ").replace("$","-").replace("%",","))
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ]  = t
                        except Exception as e :
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] = [i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]
                            
                            
                    except Exception as e: 
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")]=dict()
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",")] =[i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]

                            
                            
                    except Exception as e: 
                        dic[i[4].split()[0]]=dict()
                        dic[i[4].split()[0]] [i[3].split()[0]] =[i[1].split()[0]]
            for i in data :
                    try:
                        try :
                            desc[i[4].split()[0]] = i[5].split()[0].replace("&"," ").replace("$",",")
                        except Exception as e :
                    
                            desc[i[4].split()[0]]  = i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")           
                    except Exception as e: 
                        
                        desc[i[4].split()[0]] = dict() 
                        desc[i[4].split()[0]]= i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")        

            id = request.data["id"]
            transcript = GeneticsFpkm.objects.filter(lncRNAs__contains=id)
            a = dic
            responce = dict()
            for t in transcript :
                for i in dic.keys():
                    s=0
                    for j in dic[i].keys():
                        k = dic[i][j]
                        dat = GeneticsSerializer(t).data      
                        try:              
                            for z in k :
                                s += dat[z]
                            s/=len(k)
                            if round(s,4)==0:
                                 a[i][j]=round(s,8)
                            else:
                                a[i][j]=round(s,4)
                        except :
                            responce[dat["lncRNAs"]] = dic
                            return Response(responce)
                responce[dat["lncRNAs"]] = a 
                responce["desc"]=desc
            return Response(responce,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(
                {'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST
            )

class GetDevelopmentalFpkm(APIView):
    """
    Get fpkm data for Developmental group
    data format:
        {
            "id": "BnaA01LNG0006800.1"
        }

        test1 : {"id": "BnaA01LNG0006800.1"}
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )
    def post(self,request) -> Response:
        """no docstring"""
        try:
            data = []
            dic = dict()
            desc=dict()
            file_path = os.getcwd() + '/files/developmental/v3/'
            with open(file_path + "Developmental_Table_v3.csv", 'r') as myfile:
                for line in myfile:
                    data.append(line.split(","))

                for i in data :
                    try:
                        try :
                            t= dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] 
                            t.append(i[1].split()[0].replace("&"," ").replace("$","-").replace("%",","))
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ]  = t
                        except Exception as e :
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] = [i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]
                            
                            
                    except Exception as e: 
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")]=dict()
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",")] =[i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]

                            
                            
                    except Exception as e: 
                        dic[i[4].split()[0]]=dict()
                        dic[i[4].split()[0]] [i[3].split()[0]] =[i[1].split()[0]]
                for i in data :
                    try:
                        try :
                            desc[i[4].split()[0]] = i[5].split()[0].replace("&"," ").replace("$",",")
                        except Exception as e :
                    
                            desc[i[4].split()[0]] = i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")           
                    except Exception as e: 
                        
                        desc[i[4].split()[0]] = dict() 
                        desc[i[4].split()[0]]= i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")        

            id = request.data["id"]
            transcript = DevelopmentalFpkm.objects.filter(lncRNAs__contains=id)
            a = dic
            responce = dict()
            for t in transcript :
                for i in dic.keys():
                    s=0
                    for j in dic[i].keys():
                        k = dic[i][j]
                        dat = DevelopmentalSerializer(t).data      
                        try:              
                            for z in k :
                                s += dat[z]
                            s/=len(k)
                            if round(s,4)==0:
                                 a[i][j]=round(s,8)
                            else:
                                a[i][j]=round(s,4)
                        except :
                            responce[dat["lncRNAs"]] = dic
                            return Response(responce)

                
                responce[dat["lncRNAs"]] = a 
                responce["desc"]=desc
            return Response(responce,status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetBioticFpkm(APIView):
    """
    Get fpkm data for Biotic group
    data format:
        {
            "id": "BnaA01LNG0006800.1"
        }

        test1 : {"id": "BnaA01LNG0006800.1"}
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def post(self,request) -> Response:
        """no docstring"""
        try:
            data = []
            dic = dict()
            desc= dict()
            file_path = os.getcwd() + '/files/biotic/v3/'
            with open(file_path + "Biotic_Table_v3.csv", 'r') as myfile:
                for line in myfile:
                    data.append(line.split(","))

                for i in data :
                    try:
                        try :
                            t= dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] 
                            t.append(i[1].split()[0].replace("&"," ").replace("$","-").replace("%",","))
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ]  = t
                        except Exception as e :
                            dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",") ] = [i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]
                            
                            
                    except Exception as e: 
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")]=dict()
                        dic[i[4].split()[0].replace("&"," ").replace("$","-").replace("%",",")] [i[3].split()[0].replace("&"," ").replace("$","-").replace("%",",")] =[i[1].split()[0].replace("&"," ").replace("$","-").replace("%",",")]

                            
                            
                    
                for i in data :
                    try:
                        try :
                            desc[i[4].split()[0]] = i[5].split()[0].replace("&"," ").replace("$",",")
                        except Exception as e :
                    
                            desc[i[4].split()[0]] = i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")          
                    except Exception as e: 
                        
                        desc[i[4].split()[0]] = dict() 
                        desc[i[4].split()[0]]= i[5].split()[0].replace("&"," ").replace("$","-").replace("%",",")      

            id = request.data.get('id')
            transcript = BioticFpkm.objects.filter(lncRNAs__contains=id)
            a = dic
            responce = dict()
            for t in transcript :
                for i in dic.keys():
                    s=0
                    for j in dic[i].keys():
                        k = dic[i][j]
                        dat = BioticSerializer(t).data      
                        try:              
                            for z in k :
                                s += dat[z]
                            s/=len(k)
                            if round(s,4)==0:
                                 a[i][j]=round(s,8)
                            else:
                                a[i][j]=round(s,4)
                        except :
                            responce[dat["lncRNAs"]] = dic
                            return Response(responce)

                
                responce[dat["lncRNAs"]] = a 
                responce["desc"]=desc
            return Response(responce,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetTransposon(APIView):
    """Api for get Transposon information"""
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            search_box = request.GET.get('search', None)
            chromosome = request.GET.get('chromosome', None)
            strand = request.GET.get('strand', None)
            locus = request.GET.get('locus', None)
            page_size = request.GET.get('per_page', 10)
            page_size = int(page_size)
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            query = Q()
            if strand:
                query &= Q(strand = strand)
            if locus:
                locus = locus.split(',')
                query &= Q(start__gte = locus[0]) & Q(end__gte = locus[1])
            if chromosome:
                query &= Q(chrom = chromosome)
            if search_box:
                search_box = search_box.split(',')
                for each_query in search_box:
                    if each_query.startswith('Bna') or each_query.startswith('bna'):
                        query &= Q(lncrna_id = each_query)
                    else:
                        query &= Q(transposon_id = each_query)
            transposon_query = Transposon.objects.filter(query).order_by('id')
            result_page = paginator.paginate_queryset(transposon_query, request)
            transposon_serializer = TransposonSerializer(result_page, many=True)
            pages = transposon_query.count()/page_size if \
                 isinstance(int, type(transposon_query.count()/page_size)) else \
                    int(transposon_query.count()/page_size)+1
            return Response(
                dict(
                    data = transposon_serializer.data,
                    page = pages,
                    count = transposon_query.count()
                ),
                status=status.HTTP_200_OK
            )
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetTransposonIds(APIView):
    """Api for get Transposon ids"""
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            transposon_id_query = Transposon.objects.all().values_list('transposon_id', flat=True)
            return Response(transposon_id_query,status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetSmallRnaTarget(APIView):
    """
    Api for get SmallRna data
    Query params:
        - search=BnaC08LNG0003800,bna-miR6031
        - inhibition=Cleavage
        - expectation=2,3
        - binding_locus=100,200
        - per_page=10
        - page=2

        test1 : ?search=BnaC08LNG0003800,bna-miR6031
        test2 : ?inhibition=Cleavage&expectation=2,3&binding_locus=100,200
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            search_box = request.GET.get('search', None)
            inhibition = request.GET.get('inhibition', None)
            expectation = request.GET.get('expectation', None)
            binding_locus = request.GET.get('binding_locus', None)
            page_size = request.GET.get('per_page', 10)
            page_size = int(page_size)
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            query = Q()
            if search_box:
                search_box=search_box.split(',')
                for each_query in search_box:
                    each_query = each_query.replace(" ", "")
                    if each_query.startswith('bna-mi'):
                        query &= Q(mirna_id = each_query)
                    else:
                        query &= Q(lncrna_id = each_query)

            if inhibition:
                query &= Q(inhibition = inhibition)
            if expectation:
                expectation = expectation.split(',')
                query &= Q(expectation__gte = expectation[0]) & Q(expectation__lte = expectation[1])
            if binding_locus:
                binding_locus = binding_locus.split(',')
                query &= Q(lncrna_start__gte = binding_locus[0]) & \
                    Q(lncrna_end__lte = binding_locus[1])
            small_rna_query = SmallRnaTarget.objects.filter(query).order_by('id')
            result_page = paginator.paginate_queryset(small_rna_query, request)
            small_rna_serializer = SmallRnaTargetSerializer(result_page, many=True)
            pages = small_rna_query.count()/page_size if \
                isinstance(int, type(small_rna_query.count()/page_size)) else \
                    int(small_rna_query.count()/page_size)+1
            return Response(
                dict(
                    data = small_rna_serializer.data,
                    page = pages,
                    count = small_rna_query.count()
                ),
                status=status.HTTP_200_OK
            )
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetSmallRnaTargetIds(APIView):
    """Api for get Small Rna ids"""
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            smallrna_id_query = SmallRnaTarget.objects.all().values_list('mirna_id', flat=True)
            return Response(smallrna_id_query,status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetPremiRna(APIView):
    """
    Api for get Premi Rna information
    Query params:
        - search=BnaCnnLNG0010600,bna-miR6035
        - binding_locus=10,100
        - pre_mirna=bna-miR6031
        - per_page=10
        - page=1

        test1 : ?search=BnaCnnLNG0010600,bna-miR6035
        test2 : ?binding_locus=10,100&pre_mirna=bna-miR6031
    """

    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            search_box = request.GET.get('search', None)
            binding_locus = request.GET.get('binding_locus', None)
            pre_mirna = request.GET.get('pre_mirna', None)
            page_size = request.GET.get('per_page', 10)
            page_size = int(page_size)
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            query = Q()
            if binding_locus:
                binding_locus = binding_locus.split(',')
                query &= Q(lncrna_start__gte = binding_locus[0]) & \
                    Q(Lncrna_end__lte = binding_locus[1])
            if pre_mirna:
                query &= Q(premi_rna = pre_mirna)
            if search_box:
                search_box = search_box.split(',')
                for each_query in search_box:
                    each_query = each_query.replace(" ", "")
                    if each_query.startswith('Bna-mi') or each_query.startswith('bna-mi'):
                        query &= Q(premi_rna = each_query)
                    else :
                        query &= Q(lncrna_id = each_query)

            premi_rna_query = PremiRna.objects.filter(query).order_by('id')
            result_page = paginator.paginate_queryset(premi_rna_query, request)
            premi_rna_serializer = PremiRnaSerializer(result_page, many=True)
            pages = premi_rna_query.count()/page_size if \
                isinstance(int, type(premi_rna_query.count()/page_size)) else \
                    int(premi_rna_query.count()/page_size)+1
            return Response(
                dict(
                    data = premi_rna_serializer.data,
                    page = pages,
                    count = premi_rna_query.count()
                ),
                status=status.HTTP_200_OK
            )
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetPremiRnaIds(APIView):
    """Api for get PremiRna ids"""
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            premirna_id_query = PremiRna.objects.all().values_list('premi_rna', flat=True)
            return Response(premirna_id_query,status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetEtms(APIView):
    """Api for get Etms information"""
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            etms_query = Etms.objects.all().order_by('id')
            etms_serializer = EtmsSerializer(etms_query, many=True)
            return Response(
                dict(
                    data = etms_serializer.data,
                    count = etms_query.count()
                ),
                status=status.HTTP_200_OK
            )
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetTargetDowngene(APIView):
    """
    Api for get Premi Rna information
    Query params:
        - query=BnaA01LNG0001100
        - len_query=10,1000
        - target=BnaA01g11750D
        - len_target=10,1000
        - dg = -10,1000
        - ndg = -0.400,-0.305
        - position_query = 10,1000
        - position_target = 10,1000
        - per_page = 10
        - page = 2

        test1 : ?len_query=10,1000&len_target=10,1000&dg=-10,1000&ndg=-0.400,-0.105&position_target=10,10000
        test2 : ?target=BnaA01g11750D
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            target_query = request.GET.get('query', None)
            len_query = request.GET.get('len_query', None)
            target = request.GET.get('target', None)
            len_target = request.GET.get('len_target', None)
            target_dg = request.GET.get('dg', None)
            ndg = request.GET.get('ndg', None)
            position_query = request.GET.get('position_query', None)
            position_target = request.GET.get('position_target', None)
            page_size = request.GET.get('per_page', 10)

            page_size = int(page_size)
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            query = Q()
            if target_query:
                target_query = target_query.strip()
                query &= Q(query = target_query)
            if len_query:
                len_query = len_query.split(',')
                len_query = [each.strip() for each in len_query]
                query &= Q(length_query__gt = len_query[0]) & \
                    Q(length_query__lt = len_query[1])
            if target:
                target = target.strip()
                query &= Q(target=target)
            if len_target:
                len_target = len_target.split(',')
                len_target = [each.strip() for each in len_target]
                query &= Q(length_target__gt = len_target[0]) & \
                    Q(length_target__lt = len_target[1])
            if target_dg:
                target_dg = target_dg.split(',')
                target_dg = [each.strip() for each in target_dg]
                query &= Q(dg__gt = target_dg[0]) & \
                    Q(dg__lt = target_dg[1])
            if ndg:
                ndg = ndg.split(',')
                ndg = [each.strip() for each in ndg]
                query &= Q(ndg__gt = ndg[0]) & \
                    Q(ndg__lt = ndg[1])
            if position_query:
                position_query = position_query.split(',')
                position_query = [each.strip() for each in position_query]
                query &= Q(start_position_query__gt = position_query[0]) & \
                    Q(end_position_query__lt = position_query[1])
            if position_target:
                position_target = position_target.split(',')
                position_target = [each.strip() for each in position_target]
                query &= Q(start_position_target__gt = position_target[0]) & \
                    Q(end_position_target__lt = position_target[1])

            targetdown_query = TargetDowngene.objects.filter(query).order_by('id')
            result_page = paginator.paginate_queryset(targetdown_query, request)
            targetdown_serializer = TargetDowngeneSerializer(result_page, many=True)
            pages = targetdown_query.count()/page_size if \
                isinstance(int, type(targetdown_query.count()/page_size)) else \
                    int(targetdown_query.count()/page_size)+1
            return Response(
                dict(
                    data = targetdown_serializer.data,
                    page = pages,
                    count = targetdown_query.count()
                ),
                status=status.HTTP_200_OK
            )
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)

class GetDowngeneDescription(APIView):
    """
    Api for get Premi Rna information
    Query params:
        - gene_id=BnaUnng04540D

        test1 : ?gene_id=BnaUnng04540D
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )

    def get(self,request) -> Response:
        """no docstring"""
        try:
            gene_id = request.GET.get('gene_id', None)
            assert gene_id, 'gene_id key not found'
            query = Q(gene_id = gene_id)
            downgene_query = DowngeneDescription.objects.filter(query).order_by('id')
            downgene_serializer = DowngeneDescriptionSerializer(downgene_query, many=True)
            return Response(
                dict(
                    data = downgene_serializer.data,
                    count = downgene_query.count()
                ),
                status=status.HTTP_200_OK
            )
        except Exception as error:
            return Response({"detail":str(error)}, status=status.HTTP_400_BAD_REQUEST)
