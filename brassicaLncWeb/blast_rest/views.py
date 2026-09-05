import ast
import tempfile
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
from django.http import JsonResponse
from blast_rest import utils
import os
from blast_rest import settings as blast_settings
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.response import Response


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return



class blastn(APIView):

    def post(self,request):
        if request.method == 'POST':
            #blast_form=BlastForm
            template_init='blast/blast.html'
            template_result='blast/blast_results.html'
            blast_commandline=NcbiblastnCommandline

            extra_context=None
            r=request.data

            if True:
                try:

                    query_file_object_tmp = tempfile.NamedTemporaryFile(delete=False)
                    st = str(request.data['sequence'])

                    query_file_object_tmp.write(bytes(st, 'utf-8'))

                    evalue = float(request.data['evalue'])
                    word_size = int(request.data['word_size'])
                    database_path = blast_settings.BLAST_DB_NUCL_CHOICE[0][0]

                    standard_opt_dic = {'query': query_file_object_tmp, 'evalue': evalue, 'outfmt': 5, 'db': database_path,
                                        'word_size': word_size}


                    annotated = False

                    # none standard options:

                    sensitivity_opt_dic = ast.literal_eval(blast_settings.NUCLEOTIDE_SEARCH_SENSITIVE_CHOICE[request.data['search_sensitivity']][0])

                    blast_records__file_xml = None
                    try:

                        # blast search, parse results from temp file, put them into template for rendering.
                        blast_records__file_xml, blast_error = utils.run_blast_commands(blast_commandline,
                                                                                        **dict(standard_opt_dic,
                                                                                            **sensitivity_opt_dic))

                        if len(blast_error) > 0:
                            return JsonResponse(blast_error,safe=False)

                        else:

                            # converts blast results into objects and pack into list
                            blast_records_in_object_and_list = utils.blast_records_to_object(
                                list(NCBIXML.parse(blast_records__file_xml)))


                            if extra_context is not None:
                                blast_records_in_object_and_list = extra_context(blast_records_in_object_and_list)

                            data=[]
                            for i in blast_records_in_object_and_list :
                                for ali in i.alignments :
                                    t=dict()
                                    t["sequence"]= ali.title.split()[0].split("|")[0]
                                    t["identity"]= str(ali.best_identities())
                                    t["score"]=str(ali.best_score())
                                    t["e-value"]=str(ali.best_evalue())
                                    t["length"]=(ali.length)
                                    t["gaps"]=ali.hsp_list[0].gaps
                                    t["align_length"]=ali.hsp_list[0].align_length
                                    t["match"]=ali.hsp_list[0].match
                                    t["query_start"]=ali.hsp_list[0].query_start
                                    t["query_end"]=ali.hsp_list[0].query_end
                                    t["sbjct_start"]=ali.hsp_list[0].sbjct_start
                                    t["sbjct_end"]=ali.hsp_list[0].sbjct_end
                                    t["chop_query"]=ali.hsp_list[0].chop_query()
                                    t["score"]=ali.hsp_list[0].score
                                    t["chop_sbjct"]=ali.hsp_list[0].chop_sbjct()
                                    data.append(t)


                            return Response(data)


                    except Exception as e:
                        return Response({"detail":str(e)},status=400)
                    finally:
                        if blast_records__file_xml is not None:
                            os.remove(blast_records__file_xml.name)
                except Exception as e:
                    return Response({"detail":str(e)},status=400)

        else:
            return Response({"detail":"method wrong"},status=405)
