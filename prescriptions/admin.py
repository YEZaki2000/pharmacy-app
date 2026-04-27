from django.contrib import admin
from .models import Prescription, PrescriptionItem

# Register your models here.
class PrescriptionItemInLine(admin.TabularInline):
    model = PrescriptionItem
    extra = 1

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'status', 'klant', 'aangemaakt_op', 'datum']
    list_filter = ['status']
    inlines = [PrescriptionItemInLine]
