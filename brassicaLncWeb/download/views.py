import os
from wsgiref.util import FileWrapper

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

from django.http import HttpResponse

from lncRNA.models import lnc, abioticFpkm, bioticFpkm, geneticsFpkm, developmentalFpkm, chemicalFpkm
from .utils import exportCSV, exportTXT, exportFasta, exportGTF, exportCSVFPKM


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
                lncQuery = lnc.objects.all().values_list('id', flat=True)
                return exportGTF(list(lncQuery))
            else:
                idList = idList.split(',')
                lncQuery = lnc.objects.filter(id__in=idList).values_list('id', flat=True)
                return exportGTF(list(lncQuery))
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class downloadFile(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def get(self, request):
        try:
            '''
                Query params:
                fpkm-lnc => all_lncRNAs_fpkm.txt
                database-lnc => BrassicaLnc_Final_lncRAN_Table_Database.tsv
                fasta-lnc => Final_lncRNA_rename_V2.fa
                gtf-lnc => lncRNA.gtf
                gp(chemical):
                    chemical-lnc-fpkm => chemical_fpkm.txt
                    chemical-lnc-db => BrassIcaLnc_Tabledb_Chemical_db.tsv
                gp(genetics):
                    genetics-lnc-fpkm => genetics_fpkm.txt
                    genetics-lnc-db => BrassIcaLnc_Tabledb_Genetics_db.tsv
                gp(developmental):
                    developmental-lnc-fpkm => developmental_fpkm.txt
                    developmental-lnc-db => BrassIcaLnc_Tabledb_Developmental_db.tsv
                gp(abiotic):
                    abiotic-lnc-fpkm => abiotic_fpkm.txt
                    abiotic-lnc-db => BrassIcaLnc_Tabledb_Abiotic_db.tsv
                gp(biotic):
                    biotic-lnc-fpkm => biotic_fpkm.txt
                    biotic-lnc-db => BrassIcaLnc_Tabledb_Biotic_db.tsv
            '''
            file=request.GET.get('file',None)
            assert file,'files query param not found'
            
            os_path = os.getcwd()
            os_path+='/files'
        
            filesTemplate = {
                "fpkm-lnc":f"{os_path}/lncRNAs_fpkm.txt",
                "database-lnc":f"{os_path}/lncRANs_Table.tsv",
                "fasta-lnc" : f"{os_path}/lncRNAs.fa",
                "gtf-lnc":f"{os_path}/lncRNAs.gtf",
                "abiotic-lnc-fpkm":f"{os_path}/abiotic/v2/abiotic_fpkm.txt",
                "abiotic-lnc-db":f"{os_path}/abiotic/v2/Abiotic_Table.tsv",
                "biotic-lnc-fpkm":f"{os_path}/biotic/v2/biotic_fpkm.txt",
                "biotic-lnc-db":f"{os_path}/biotic/v2/Biotic_Table.tsv",
                "chemical-lnc-fpkm":f"{os_path}/chemical/v2/chemical_fpkm.txt",
                "chemical-lnc-db":f"{os_path}/chemical/v2/Chemical_Table.tsv",
                "developmental-lnc-fpkm":f"{os_path}/developmental/v2/developmental_fpkm.txt",
                "developmental-lnc-db":f"{os_path}/developmental/v2/Developmental_Table.tsv",
                "genetics-lnc-fpkm":f"{os_path}/genetics/v2/genetics_fpkm.txt",
                "genetics-lnc-db":f"{os_path}/genetics/v2/Genetics_Table.tsv",

            }

            filePath = filesTemplate[file]
            fileHnadeler = open(filePath, 'r')
            fileName = filesTemplate[file].split('/')[-1]

            response = HttpResponse(FileWrapper(fileHnadeler),
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="{}"'.format(fileName)})
            return response
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class downloadCSVFpkm(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)

    def get(self, request):
        try:
            tranId  = request.GET.get('id', None)
            groupName = request.GET.get('group', None)
            assert tranId, 'transcript id key not found'
            assert groupName, 'group name key not found'
            if groupName == "chemical":
                fpkmQuery = chemicalFpkm.objects.filter(lncRNAs=tranId).values()[0]
                if fpkmQuery:
                    return exportCSVFPKM(fpkmQuery)
            elif groupName == "developmental":
                fpkmQuery = developmentalFpkm.objects.filter(lncRNAs=tranId).values()[0]
                if fpkmQuery:
                    return exportCSVFPKM(fpkmQuery)
            elif groupName == "abiotic":
                fpkmQuery = abioticFpkm.objects.filter(lncRNAs=tranId).values()[0]
                if fpkmQuery:
                    return exportCSVFPKM(fpkmQuery)
            elif groupName == "biotic":
                fpkmQuery = bioticFpkm.objects.filter(lncRNAs=tranId).values()[0]
                if fpkmQuery:
                    return exportCSVFPKM(fpkmQuery)
            elif groupName == "genetics":
                fpkmQuery = geneticsFpkm.objects.filter(lncRNAs=tranId).values()[0]
                if fpkmQuery:
                    return exportCSVFPKM(fpkmQuery)
            else:
                return Response({'details': "group name not correct"}, 
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            if not fpkmQuery:
                return Response({'details': "Query does not exist"}, 
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
