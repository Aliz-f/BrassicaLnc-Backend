from django.contrib import admin
from .models import lnc, gtf, chemicalFpkm, abioticFpkm

# Register your models here.

admin.site.register(lnc)
admin.site.register(gtf)
admin.site.register(chemicalFpkm)
admin.site.register(abioticFpkm)

