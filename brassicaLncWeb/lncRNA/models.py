from this import d
from django.db import models

# Create your models here.

class lnc (models.Model):
    geneId = models.CharField(verbose_name="Gene ID", max_length=70, null=False)
    transcriptId = models.CharField(verbose_name="Transcript ID", max_length=70, null=False)
    stringTieId  = models.CharField(verbose_name="StringTie ID", max_length=70, null=False)
    chr = models.CharField(verbose_name="Chr", max_length=20, null=False)
    location = models.CharField(verbose_name="Location", max_length=70, null=False)
    locStart = models.IntegerField(verbose_name='location start', null=False)
    locEnd = models.IntegerField(verbose_name='location End', null=False)
    length = models.PositiveIntegerField(verbose_name="Length", null=False)
    classification = models.CharField(verbose_name="Classification", max_length=5, null=False)
    exonNumber = models.PositiveIntegerField(verbose_name="Exon number", null=False)
    sequence = models.TextField(verbose_name="Fasta", null=False)
    
    def __str__(self):
        return self.geneId

class gtf(models.Model):
    gene_id = models.CharField(verbose_name="Gene_id", null=False, max_length=100)
    transcript_id = models.CharField(verbose_name="Transcript_id", null=False, max_length=100)
    stringTie = models.CharField(verbose_name="StringTie", null=False, max_length=100)
    exon = models.CharField(verbose_name="Exon", null=False, max_length=100)
    locStart = models.IntegerField(verbose_name="Location start", null=False)
    locEnd = models.IntegerField(verbose_name="Location end", null=False)
    number = models.IntegerField(verbose_name="Number", null=False)
    symbol1 = models.CharField(verbose_name="Symbol 1", null=False, max_length=100)
    symbol2 = models.CharField(verbose_name="Symbol 2", null=False, max_length=100)
    exon_number = models.IntegerField(verbose_name="Exon_Number", null=False)
    chr = models.CharField(verbose_name="Chr", null=False, max_length=100)

    def __str__(self):
        return self.transcript_id