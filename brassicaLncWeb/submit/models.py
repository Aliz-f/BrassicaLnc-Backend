"""LncRna project model for submit app"""
from django.db import models

# Create your models here.
class SubmitedData(models.Model):
    """Submitted data model"""
    email=models.EmailField(
        verbose_name="Email",
        max_length=50
    )
    chromosome = models.CharField(
        verbose_name="Chromosome",
        max_length=80
    )
    location=models.CharField(
        verbose_name="Location",
        max_length=80
    )
    strand=models.CharField(
        verbose_name="Strand",
        max_length=10
    )
    sequence = models.TextField(
        verbose_name="Sequence"
    )
    name=models.CharField(
        verbose_name="Name",
        max_length=50,
        null=True,
        blank=True
    )
    expressionValue=models.CharField(
        verbose_name="Expression Value",
        max_length=50,
        null=True,
        blank=True
    )
    sampleInformation=models.CharField(
        verbose_name="Sample Information",
        max_length=50,
        null=True,
        blank=True
    )
    experimentalDesign=models.CharField(
        verbose_name="Experimental Design",
        max_length=50,
        null=True,
        blank=True
    )
    lncRNAFunction=models.CharField(
        verbose_name="LncRNA Function",
        max_length=50,
        null=True,
        blank=True
    )
    reference=models.CharField(
        verbose_name="Reference",
        max_length=50,
        null=True,
        blank=True
    )
    otherInformation=models.TextField(
        verbose_name="Other Information",
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        """no docstring"""
        return f"data submitted form : {self.email}"
