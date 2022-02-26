from django.http import HttpResponse
import csv

def exportCSV(lncList):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="lncRNA.csv"'},
    )

    writer = csv.writer(response)
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