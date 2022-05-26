from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([relationshipBetween_Chr_Gene_LncRNA,filtrationStepsLncRNAIdentificationPipeline,subdivisionLncRNAsAccordingClassCodes])
