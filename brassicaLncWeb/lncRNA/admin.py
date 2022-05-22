from django.contrib import admin
from .models import lnc, gtf, chemicalFpkm, abioticFpkm, geneticsFpkm, developmentalFpkm, bioticFpkm

# Register your models here.

admin.site.register(lnc)
admin.site.register(gtf)
admin.site.register(chemicalFpkm)
admin.site.register(abioticFpkm)
admin.site.register(geneticsFpkm)
admin.site.register(developmentalFpkm)
admin.site.register(bioticFpkm)

