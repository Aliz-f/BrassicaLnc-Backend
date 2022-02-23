from this import d
from django.db import models

# Create your models here.

class lnc (models.Model):
    geneId = models.CharField(verbose_name="Gene ID", max_length=70, null=False)
    transcriptId = models.CharField(verbose_name="Transcript ID", max_length=70, null=False)
    stringTieId  = models.CharField(verbose_name="StringTie ID", max_length=70, null=False)
    chr = models.CharField(verbose_name="Chr", max_length=20, null=False)
    location = models.CharField(verbose_name="Location", max_length=70, null=False)
    length = models.PositiveIntegerField(verbose_name="Length", null=False)
    classification = models.CharField(verbose_name="Classification", max_length=5, null=False)
    exonNumber = models.PositiveIntegerField(verbose_name="Exon number", null=False)
    sequence = models.TextField(verbose_name="Fasta", null=False)
    
    def __str__(self):
        return self.geneId