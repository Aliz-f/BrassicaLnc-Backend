"""LncRna project urls for lncRNA app"""
from django.urls import path
from .views import (GetTranscripts, GetEachTranscript,
    GetChemicalFpkm, GetAbioticFpkm, GetGeneticsFpkm,
    GetDevelopmentalFpkm, GetBioticFpkm, GetTransposon,
    GetTransposonIds, GetSmallRnaTarget, GetSmallRnaTargetIds,
    GetPremiRna, GetPremiRnaIds, GetEtms
)

urlpatterns = [

    #*transcripts
    path('transcripts/', GetTranscripts.as_view(), name='transcripts'),
    path("transcript/each/", GetEachTranscript.as_view(), name='eachTranscript'),
    #*group_plots
    path("chemical/",GetChemicalFpkm.as_view(),name="chemical"),
    path("abiotic/",GetAbioticFpkm.as_view(),name="Abiotic"),
    path("genetics/",GetGeneticsFpkm.as_view(),name="genetics"),
    path("developmental/",GetDevelopmentalFpkm.as_view(),name="developmental"),
    path("biotic/",GetBioticFpkm.as_view(),name="biotic"),
    #*multi_omics
    #transposon
    path("transposon/", GetTransposon.as_view(),name="transposon"),
    path("transposon/ids/", GetTransposonIds.as_view(),name="transposon_ids"),
    #smallRNA
    path("small_rna_target/", GetSmallRnaTarget.as_view(),name="small_rna"),
    path("small_rna_target/ids/", GetSmallRnaTargetIds.as_view(),name="small_rna_ids"),
    #premiRNA
    path("premi_rna/", GetPremiRna.as_view(),name="premi_rna"),
    path("premi_rna/ids/", GetPremiRnaIds.as_view(),name="premi_rna_ids"),
    #etms
    path("etms/", GetEtms.as_view(),name="etms"),

]
