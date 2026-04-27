from django.contrib import admin
from .models import Category, Supplier, Medicine

# Register your models here.
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['naam', 'dosering', 'voorraad', 'prijs', 'voorraad_laag']
    list_filter = ['categorie', 'vereist_recept']
    search_fields = ['naam']

admin.site.register(Category)
admin.site.register(Supplier)
