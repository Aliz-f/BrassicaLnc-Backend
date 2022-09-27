"""LncRna project utils for download app"""
import csv
from django.http import HttpResponse
from lncRNA.models import Gtf, Lnc

def export_csv(lnc_list) -> HttpResponse:
    """generate cvs file format"""
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.csv"'},
    )
    writer = csv.writer(response, delimiter='\t')
    writer.writerow(
        [
            'geneId', 'transcriptId',
            'stringTieId', 'chr', 'location',
            'length', 'exonNumber', 'classification'
        ]
    )
    for value in lnc_list:
        writer.writerow(
            [
                value.geneId, value.transcriptId,
                value.stringTieId, value.chr,
                value.location, value.length,
                value.exonNumber, value.classification
            ]
        )
    return response

def export_txt(lnc_list) -> HttpResponse:
    """generate txt file format"""
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.txt"'},
    )
    writer = csv.writer(response)
    writer.writerow(
        [
            'geneId', 'transcriptId',
            'stringTieId', 'chr',
            'location', 'length',
            'exonNumber', 'classification'
        ]
    )
    for value in lnc_list:
        writer.writerow(
            [
                value.geneId, value.transcriptId,
                value.stringTieId, value.chr,
                value.location, value.length,
                value.exonNumber, value.classification
            ]
        )
    return response

def export_fasta(lnc_list) -> HttpResponse:
    """generate fasta file format"""
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.fa"'},
    )
    writer = csv.writer(response)
    for value in lnc_list:
        temp = f">{value.transcriptId}"
        writer.writerow([temp])
        writer.writerow([value.sequence])
    return response

def export_gtf(lnc_list) -> HttpResponse:
    """generate gtf file format"""
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.gtf"'},
    )
    writer = csv.writer(response)
    lnc_query = Lnc.objects.filter(id__in = lnc_list)
    for value in lnc_query:
        gtf_query = Gtf.objects.filter(transcript_id = value.stringTieId)
        for each_gtf in gtf_query:
            str_temp = f"{each_gtf.chromosome}\t{each_gtf.stringTie}\t{each_gtf.exon}\t{each_gtf.locStart}\t{each_gtf.locEnd}\t{each_gtf.number}\t{each_gtf.strand1}\t{each_gtf.strand2}\tgene_id {each_gtf.gene_id}; \transcript_id {each_gtf.transcript_id}; exon_number {each_gtf.exon_number}; "
            writer.writerow([str_temp])
    return response

def export_csv_fpkm(fpkm) -> HttpResponse:
    """generate cvs fpkm file format"""
    fields_list=[]
    value_list =[]
    for key in fpkm.keys():
        fields_list.append(key)
    for value in fpkm.values():
        value_list.append(value)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{value_list[1]}.csv"'},
    )
    writer = csv.writer(response, delimiter='\t')
    writer.writerow(fields_list)
    writer.writerow(value_list)
    return response
