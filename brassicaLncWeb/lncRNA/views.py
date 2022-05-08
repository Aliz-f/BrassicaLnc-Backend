from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination

from .serializer import * 
from .models import *
import csv
import time

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

class eachTranscript(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def post(self, request):
        try:
            data = request.data
            transcript = data.get('tranId', None)
            assert transcript, 'tranId not found'
            lncQuery = lnc.objects.get(transcriptId=transcript)
            gtfQuery = gtf.objects.filter(transcript_id=lncQuery.stringTieId)
            lncSer = lncSerializer(lncQuery)
            gtfSer = gtfSerializer(gtfQuery,many=True)
            response = {}
            response['lnc'] = lncSer.data
            response['gtf'] = gtfSer.data
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class chemical(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def post(self,request):
        try:
            data = []
            dic = dict()
            with open("lncRNA/files/Tabledb_Chemical_db.csv", 'r') as myfile:
                for line in myfile:
                    data.append(line.split(","))

                for i in data :
                    #print(i) #done iaa 
                    #break
                    try:
                        try :
                            
                            t= dic[i[4].split()[0]] [i[3].split()[0] +"_"+ i[2].split()[0]] 
                            #print(dic[i[4].split()[0]],"1",t)
                            t.append(i[1].split()[0])
                            #print(dic[i[4].split()[0]],"2",t)
                            dic[i[4].split()[0]] [i[3].split()[0] +"_"+ i[2].split()[0] ]  =t
                        except Exception as e :
                            #t = dic[i[4].split()[0]]
                            #print(i[:4])
                            dic[i[4].split()[0]] [i[3].split()[0] +"_"+ i[2].split()[0] ] = [i[1].split()[0]]
                            #print("dd",":",e)
                            
                    except Exception as e: 
                        dic[i[4].split()[0]]=dict()
                        dic[i[4].split()[0]] [i[3].split()[0] +"_"+ i[2].split()[0] ] =[i[1].split()[0]]
                        #print(e)

            id = request.data["id"]
            transcript = chemicalFpkm.objects.filter(lncRNAs__contains=id)
            a = dic
            #print(dic["IAA_treatment"])
            #return Response({"1":1})
            responce = dict()
            #print(dic)
            #{"id":"BnaCnnLNG0002300"}
            #return Response(1)
            for t in transcript :
                for i in dic.keys():
                    s=0
                    for j in dic[i].keys():
                        k = dic[i][j]
                        #print(dic,"i",i,"  j :",j, "ppp   ", dic[i][j])
                        #return Response({"1":1})
                        #print(t)
                        dat = chemicalSerializer(t).data      
                        try:              
                            for z in k :
                                s += dat[z]
                            s/=len(k)
                            a[i][j]=s
                        except :
                            #print(k , "i:",i,"  j:",j)
                            #print(dic)
                            responce[dat["lncRNAs"]] = dic
                            #print(responce)
                            return Response(responce)

                #print(dat["lncRNAs"])
                #return Response({"1":1})
                responce[dat["lncRNAs"]] = a 
            #print(a)
            return Response(responce,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class create_chemical_db(APIView):
    def post(self, request):
        try:
            ser = chemicalSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class create_abiotic_db(APIView):
    def post(self, request):
        try:
            ser = abioticSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class create_genetics_db(APIView):
    def post(self, request):
        try:
            ser = geneticsSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class create_developmental_db(APIView):
    def post(self, request):
        try:
            ser = developmentalSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
