from django.db import models
from accounts.models import CustomUser
from encrypted_model_fields.fields import EncryptedCharField

# Create your models here.

class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profiel')
    geboortedatum = models.DateField(null=True, blank=True)
    telefoon = models.CharField(max_length=20, blank=True)
    adres = models.TextField(blank=True)
    allergiëen = models.TextField(blank=True)
    aangemaakt_op = models.DateTimeField(auto_now_add=True)
    bsn = EncryptedCharField(max_length=9, blank=True, null=True, help_text='9 cijfers')

    def __str__(self):
        return f"Profiel van {self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = 'Klantprofiel'
