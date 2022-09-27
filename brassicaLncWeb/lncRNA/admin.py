"""LncRna project admin panel config for lncRNA app"""
from django.contrib import admin
from .models import (Lnc, Gtf, ChemicalFpkm,
    AbioticFpkm, GeneticsFpkm, DevelopmentalFpkm,
    BioticFpkm, Transposon, SmallRnaTarget, PremiRna, Etms, TargetDowngene,
    DowngeneDescription,
)

# Register your models here.

class LncAdmin(admin.ModelAdmin):
    """Lnc model config for admin panel."""
    list_display= [
        "id",
        "geneId",
        "transcriptId",
        "stringTieId",
        "chr",
        "location",
        "length",
        "classification",
        "exonNumber",
    ]
    fields = [
        "id",
        "geneId",
        "transcriptId",
        "stringTieId",
        "chr",
        "location",
        "locStart",
        "locEnd",
        "length",
        "classification",
        "exonNumber",
        "sequence",
    ]
    readonly_fields = [
        "id",
    ]
    search_fields = [
        "id",
        "geneId",
        "transcriptId",
        "stringTieId",
        "chr",
        "location",
        "length",
        "classification",
        "exonNumber",
    ]
    list_filter = [
        "classification",
        "chr",
    ]
    list_per_page = 20

class GtfAdmin(admin.ModelAdmin):
    """Gtf model config for admin panel."""
    list_display= [
        "id",
        "gene_id",
        "transcript_id",
        "stringTie",
        "exon",
        "locStart",
        "locEnd",
        "number",
        "strand1",
        "strand2",
        "exon_number",
        "chromosome",
    ]
    fields = [
        "id",
        "gene_id",
        "transcript_id",
        "stringTie",
        "exon",
        "locStart",
        "locEnd",
        "number",
        "strand1",
        "strand2",
        "exon_number",
        "chromosome",
    ]
    readonly_fields = [
        "id",
    ]
    search_fields = [
        "id",
        "gene_id",
        "transcript_id",
        "stringTie",
        "exon",
        "locStart",
        "locEnd",
        "number",
        "strand1",
        "strand2",
        "exon_number",
        "chromosome",
    ]
    list_filter = [
        "exon",
        "strand1",
        "strand2"
    ]
    list_per_page = 20

class TransposonAdmin(admin.ModelAdmin):
    """Transposon model config for admin panel."""
    list_display= [
        "id",
        "lncrna_id",
        "transposon_id",
        "chrom",
        "strand",
        "start",
        "end",
        "overlap",
    ]
    fields = [
        "id",
        "lncrna_id",
        "transposon_id",
        "chrom",
        "strand",
        "start",
        "end",
        "overlap",
    ]
    readonly_fields = [
        "id",
    ]
    search_fields = [
        "id",
        "lncrna_id",
        "transposon_id",
        "chrom",
        "strand",
        "start",
        "end",
        "overlap",
    ]
    list_filter = [
        "transposon_id",
    ]
    list_per_page = 20

class SmallRNATargetAdmin(admin.ModelAdmin):
    """Small Rna model config for admin panel."""
    list_display= [
        "id",
        "lncrna_id",
        "mirna_id",
        "expectation",
        "lncrna_start",
        "lncrna_end",
        "mirna_start",
        "mirna_end",
        "inhibition",
    ]
    fields = [
        "id",
        "lncrna_id",
        "mirna_id",
        "expectation",
        "lncrna_start",
        "lncrna_end",
        "mirna_start",
        "mirna_end",
        "inhibition",
        "lncrna_aligned_fragment",
        "mirna_aligned_fragment"
    ]
    readonly_fields = [
        "id",
    ]
    search_fields = [
        "id",
        "lncrna_id",
        "mirna_id",
        "expectation",
        "lncrna_start",
        "lncrna_end",
        "mirna_start",
        "mirna_end",
        "inhibition",
    ]
    list_filter = [
        "mirna_id",
    ]
    list_per_page = 20

class PremiRNAAdmin(admin.ModelAdmin):
    """Premi Rna model config for admin panel."""
    list_display= [
        "id",
        "lncrna_id",
        "premi_rna",
        "identity",
        "alignment_length",
        "mismatches",
        "lncrna_start",
        "Lncrna_end",
        "premi_rna_start",
        "premi_rna_end",
        "e_value",
        "bitscore",
        "structure",
    ]
    fields = [
        "id",
        "lncrna_id",
        "premi_rna",
        "identity",
        "alignment_length",
        "mismatches",
        "lncrna_start",
        "Lncrna_end",
        "premi_rna_start",
        "premi_rna_end",
        "e_value",
        "bitscore",
        "structure",
    ]
    readonly_fields = [
        "id",
        "structure",
    ]
    search_fields = [
        "id",
        "lncrna_id",
        "premi_rna",
        "identity",
        "alignment_length",
        "mismatches",
        "lncrna_start",
        "Lncrna_end",
        "premi_rna_start",
        "premi_rna_end",
        "e_value",
        "bitscore",
        "structure",
    ]
    list_filter = [
        "premi_rna",
        "structure",
    ]
    list_per_page = 10

class EtmsAdmin(admin.ModelAdmin):
    """Etms model config for admin panel."""
    list_display= [
        "id",
        "lncrna_id",
        "mirna_id",
        "score",
        "lncrna_start",
        "lncrna_end",
        "mirna_start",
        "mirna_end",
    ]
    fields = [
        "id",
        "lncrna_id",
        "mirna_id",
        "score",
        "lncrna_start",
        "lncrna_end",
        "mirna_start",
        "mirna_end",
        "alignment",
        "lnc_alignment",
        "mirna_alignment",
    ]
    readonly_fields = [
        "id",
    ]
    search_fields = [
        "id",
        "lncrna_id",
        "mirna_id",
        "score",
        "lncrna_start",
        "lncrna_end",
        "mirna_start",
        "mirna_end",
        "alignment",
        "lnc_alignment",
        "mirna_alignment",
    ]
    list_filter = [
        "mirna_id",
    ]
    list_per_page = 10


class TargetDowngeneAdmin(admin.ModelAdmin):
    """Etms model config for admin panel."""
    list_display= [
        "id",
        "query",
        "length_query",
        "target",
        "length_target",
        "dg",
        "ndg",
        "start_position_query",
        "end_position_query",
        "start_position_target",
        "end_position_target",
    ]
    fields = [
        "id",
        "query",
        "length_query",
        "target",
        "length_target",
        "dg",
        "ndg",
        "start_position_query",
        "end_position_query",
        "start_position_target",
        "end_position_target",
    ]
    readonly_fields = [
        "id",
    ]
    search_fields = [
        "id",
        "query",
        "length_query",
        "target",
        "length_target",
        "dg",
        "ndg",
        "start_position_query",
        "end_position_query",
        "start_position_target",
        "end_position_target",
    ]
    list_per_page = 10

class DowngeneDescriptionAdmin(admin.ModelAdmin):
    """Etms model config for admin panel."""
    list_display= [
        "id",
        "gene_id",
        "chromosome",
        "start",
        "stop",
        "strand",
        "description",
    ]
    fields = [
        "id",
        "gene_id",
        "chromosome",
        "start",
        "stop",
        "strand",
        "description",
    ]
    readonly_fields = [
        "id",
    ]
    search_fields = [
        "id",
        "gene_id",
        "chromosome",
        "start",
        "stop",
        "strand",
        "description",
    ]
    list_per_page = 10

admin.site.register(Lnc, LncAdmin)
admin.site.register(Gtf, GtfAdmin)
admin.site.register(ChemicalFpkm)
admin.site.register(AbioticFpkm)
admin.site.register(GeneticsFpkm)
admin.site.register(DevelopmentalFpkm)
admin.site.register(BioticFpkm)
admin.site.register(Transposon, TransposonAdmin)
admin.site.register(SmallRnaTarget, SmallRNATargetAdmin)
admin.site.register(PremiRna, PremiRNAAdmin)
admin.site.register(Etms, EtmsAdmin)
admin.site.register(TargetDowngene, TargetDowngeneAdmin)
admin.site.register(DowngeneDescription, DowngeneDescriptionAdmin)
