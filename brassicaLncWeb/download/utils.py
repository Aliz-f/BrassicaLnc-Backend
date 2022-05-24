from django.http import HttpResponse
import csv
from lncRNA.models import gtf, lnc

def exportCSV(lncList):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.csv"'},
    )

    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['geneId', 'transcriptId', 'stringTieId', 'chr', 'location', 'length', 'exonNumber', 'classification' ])
    for value in lncList:
        writer.writerow([value.geneId, value.transcriptId, value.stringTieId, value.chr, value.location, value.length, value.exonNumber, value.classification])

    return response

def exportTXT(lncList):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.txt"'},
    )

    writer = csv.writer(response)
    writer.writerow(['geneId', 'transcriptId', 'stringTieId', 'chr', 'location', 'length', 'exonNumber', 'classification' ])
    for value in lncList:
        writer.writerow([value.geneId, value.transcriptId, value.stringTieId, value.chr, value.location, value.length, value.exonNumber, value.classification])

    return response

def exportFasta(lncList):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.fa"'},
    )

    writer = csv.writer(response)
    for value in lncList:
        temp = '>{}'.format(value.transcriptId)
        writer.writerow([temp])
        writer.writerow([value.sequence])

    return response

def exportGTF(lncList):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.gtf"'},
    )

    writer = csv.writer(response)
    lncQuery = lnc.objects.filter(id__in = lncList)
    for value in lncQuery:
        gtfQuery = gtf.objects.filter(transcript_id = value.stringTieId)
        for eachGTF in gtfQuery:
            strTemp = """{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\tgene_id {}; transcript_id {}; exon_number {}; """.format(
                eachGTF.chromosome, eachGTF.stringTie, 
                eachGTF.exon, eachGTF.locStart, eachGTF.locEnd,
                eachGTF.number, eachGTF.strand1, eachGTF.strand2,
                eachGTF.gene_id, eachGTF.transcript_id, eachGTF.exon_number)
            writer.writerow([strTemp])

    return response