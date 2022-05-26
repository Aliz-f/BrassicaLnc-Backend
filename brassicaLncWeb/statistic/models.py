from json import JSONEncoder
from django.db import models

# Create your models here.

class relationshipBetween_Chr_Gene_LncRNA(models.Model):
    name = models.CharField(verbose_name="Table name", max_length=250, blank=False, null=False)
    data = models.JSONField(verbose_name="Data", blank=False, null=False)

class filtrationStepsLncRNAIdentificationPipeline(models.Model):
    name = models.CharField(verbose_name="Table name", max_length=250, blank=False, null=False)
    data = models.JSONField(verbose_name="Data", blank=False, null=False)

class subdivisionLncRNAsAccordingClassCodes(models.Model):
    name = models.CharField(verbose_name="Table name", max_length=250, blank=False, null=False)
    data = models.JSONField(verbose_name="Data", blank=False, null=False)


# {
#     "The quantitative relationship between Chromosome, Gene and LncRNA": {
#         "chromosome":41,
#         "mRNA":101040,
#         "lncRNA":1856
#     },
#     "The results of filtration steps in the lncRNA identification pipeline. Numbers represent the total number of transcripts filtered out in each step.":{
#         "Potential novel transripts (Class codes: i, u, x, o, e)":31777,
#         "Transcripts with length > 200 bp and < 15 kb":30905,
#         "Transcripts with FPKM > 0.5 in at least 495 samples":5990,
#         "Transcripts after filter out tRNAs and rRNAs":5947,
#         "Noncoding transcripts predicted by CPC2":4766,
#         "LncRNAs predicted by PLncPRO, FEElnc, and CREMA":2321,
#         "Transcripts with no significant hit against UniProt, Pfam, and Rfam.":1852,
#         "Reliably expressed lncRNAs":0
#     },
#     "Subdivision of lncRNAs according to the class codes (“u,” “x,” “i,” “o,” and “e”)":
#     {
#         "intronic lncRNAs (i)":25,
#         "generic exonic overlap lncRNAs with reference transcripts (o)":178,
#         "intergenic lncRNAs (u)":1645,
#         "antisense lncRNAs (x)":0,
#     }
# }