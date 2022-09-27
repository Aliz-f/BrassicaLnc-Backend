"""LncRna project models for statistic app"""
from django.db import models

class RelationshipBetweenChrGeneLncRna(models.Model):
    """The quantitative relationship between Chromosome, Gene and LncRNA"""
    name = models.CharField(
        verbose_name="Table name",
        max_length=250,
        blank=False,
        null=False
    )
    data = models.JSONField(
        verbose_name="Data",
        blank=False,
        null=False
    )

class FiltrationStepsLncRnaIdentificationPipeline(models.Model):
    """The results of filtration steps in the lncRNA identification pipeline.
    Numbers represent the total number of transcripts filtered out in each step."""
    name = models.CharField(
        verbose_name="Table name",
        max_length=250,
        blank=False,
        null=False
    )
    data = models.JSONField(
        verbose_name="Data",
        blank=False,
        null=False
    )

class SubdivisionLncRnasAccordingClassCodes(models.Model):
    """Subdivision of lncRNAs according to the class codes (“u,” “x,” “i,” “o,” and “e”)"""
    name = models.CharField(
        verbose_name="Table name",
        max_length=250,
        blank=False,
        null=False
    )
    data = models.JSONField(
        verbose_name="Data",
        blank=False,
        null=False
    )
