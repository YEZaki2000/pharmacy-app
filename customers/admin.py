from django.contrib import admin
from .models import CustomerProfile

# Register your models here.
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefoon', 'geboortedatum']
    search_fields = ['uder__username', 'user__email']
    readonly_fields = ['aangemaakt_op']

