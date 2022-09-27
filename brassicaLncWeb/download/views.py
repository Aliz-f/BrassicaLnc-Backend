"""LncRna project views for download app"""
import os
from wsgiref.util import FileWrapper

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

from django.http import HttpResponse

from lncRNA.models import (
                Lnc, AbioticFpkm,
                BioticFpkm, GeneticsFpkm,
                DevelopmentalFpkm, ChemicalFpkm, PremiRna)
from .utils import export_csv, export_txt, export_fasta, export_gtf, export_csv_fpkm


# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """CsrfExempt Session Authentication"""
    def enforce_csrf(self, request):
        return

# Create your views here.
class LncDownloadCsvFormat(APIView):
    """
    Download lncs in csv format
    Query param:
        - ids (Transcripts database id)
        - NONE (Download all lncs)

        test1: ?ids=1,2,3,4,5,6,7,8,9,
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
            id_list = request.GET.get('ids', None)
            if id_list is None:
                lnc_query = Lnc.objects.all()
                return export_csv(list(lnc_query))
            id_list = id_list.split(',')
            lnc_query = Lnc.objects.filter(id__in=id_list)
            return export_csv(list(lnc_query))
        except Exception as error:
            return Response(
                {'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST
            )

class LncDownloadTxtFormat(APIView):
    """
    Download Lncs in txt format
    Query param:
        - ids (Transcripts database id)
        - NONE (Download all lncs)

        test1 : ?ids=1,2,3,4,5,6,7,8,9,
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
            id_list = request.GET.get('ids', None)
            if id_list is None:
                lnc_query = Lnc.objects.all()
                return export_txt(list(lnc_query))
            id_list = id_list.split(',')
            lnc_query = Lnc.objects.filter(id__in=id_list)
            return export_txt(list(lnc_query))
        except Exception as error:
            return Response(
                {'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST
            )

class LncDownloadFastaFormat(APIView):
    """
    Download Lncs in fasta format
    Query param:
        - ids (Transcripts database id)
        - NONE (Download all lncs)

        test1 : ?ids=1,2,3,4,5,6,7,8,9,
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
            id_list = request.GET.get('ids', None)
            if id_list is None:
                lnc_query = Lnc.objects.all()
                return export_fasta(list(lnc_query))
            id_list = id_list.split(',')
            lnc_query = Lnc.objects.filter(id__in=id_list)
            return export_fasta(list(lnc_query))
        except Exception as error:
            return Response(
                {'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST
            )

class LncDownloadGtfFormat(APIView):
    """
    Download Lncs in gtf format
    Query param:
        - ids (Transcripts database id)
        - NONE (Download all lncs)

        test1 : ?ids=1,2,3,4,5,6,7,8,9,

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
            id_list = request.GET.get('ids', None)
            if id_list is None:
                lnc_query = Lnc.objects.all().values_list('id', flat=True)
                return export_gtf(list(lnc_query))
            id_list = id_list.split(',')
            lnc_query = Lnc.objects.filter(id__in=id_list).values_list('id', flat=True)
            return export_gtf(list(lnc_query))
        except Exception as error:
            return Response(
                {'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST
            )

class DownloadAllFiles(APIView):
    """ Download all files
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

        test1 : ?file=fpkm-lnc
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
            file=request.GET.get('file',None)
            assert file,'files query param not found'
            file = file.replace(' ','')
            os_path = os.getcwd() + '/files'
            files_address = {
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
            file_path = files_address[file]
            with open(file_path, 'rb') as file_handeler:
                file_name = files_address[file].split('/')[-1]
                response = HttpResponse(FileWrapper(file_handeler),
                content_type='text/csv',
                headers={'Content-Disposition': f'attachment; filename="{file_name}"'})
                return response
        except Exception as erorr:
            return Response(
                {'detail': str(erorr)}, status=status.HTTP_400_BAD_REQUEST
            )

class GroupDownloadCsvFpkm(APIView):
    """
        Download group fpkm in csv format
        Query params :
            - id=BnaCnnLNG0016000.1
            - group= ( genetics | chemical | biotic | abiotic | developmental)

            test1 : ?id=BnaCnnLNG0016000.1&group=chemical
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
            tran_id  = request.GET.get('id', None)
            group_name = request.GET.get('group', None)
            assert tran_id, 'transcript id key not found'
            assert group_name, 'group name key not found'
            if group_name == "chemical":
                fpkm_query = ChemicalFpkm.objects.filter(lncRNAs=tran_id).values()[0]
            elif group_name == "developmental":
                fpkm_query = DevelopmentalFpkm.objects.filter(lncRNAs=tran_id).values()[0]
            elif group_name == "abiotic":
                fpkm_query = AbioticFpkm.objects.filter(lncRNAs=tran_id).values()[0]
            elif group_name == "biotic":
                fpkm_query = BioticFpkm.objects.filter(lncRNAs=tran_id).values()[0]
            elif group_name == "genetics":
                fpkm_query = GeneticsFpkm.objects.filter(lncRNAs=tran_id).values()[0]
            else:
                return Response({'details': "group name not correct"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            if fpkm_query:
                return export_csv_fpkm(fpkm_query)
            return Response(
                {'details': "Query does not exist"},status=status.HTTP_404_NOT_FOUND
                )
        except Exception as error:
            return Response(
                {'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST
            )

class DownloadStructurePremiRna(APIView):
    """
    Download structure for premiRNA in multi_omics
    Query param:
        - transcript=BnaA01LNG0004100

        test1 : ?transcript=BnaA01LNG0004100
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
            transcript_id = request.GET.get('transcript', None)
            assert transcript_id, 'transcript key id not found'
            if PremiRna.objects.filter(lncrna_id = transcript_id).exists():
                os_path = os.getcwd()
                os_path+='/files/multi_omics/premiRNA/structure/'
                file_address = os_path + str(transcript_id) + str('.pdf')
                print(file_address)
                if os.path.exists(file_address):
                    with open(file_address, 'rb') as file_handeler:
                        response = HttpResponse(FileWrapper(file_handeler),
                        content_type='application/pdf',
                        headers=
                            {'Content-Disposition': f'attachment; filename="{transcript_id}.pdf"'})
                        return response
                return Response(
                    {'detail':'structure not found'}, status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                {'detail':'permiRNA not found'}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as erorr:
            return Response(
                {'detail': str(erorr)}, status=status.HTTP_400_BAD_REQUEST
            )
