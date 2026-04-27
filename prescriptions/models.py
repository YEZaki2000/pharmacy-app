from django.db import models
from accounts.models import CustomUser
from inventory.models import Medicine

# Create your models here.

class Prescription(models.Model):
    class Status(models.TextChoices):
        NIEUW = 'nieuw', 'Nieuw'
        IN_BEHANDELING = 'in_behandeling', 'Im behandeling'
        KLAAR = 'klaar', 'Klaar'
        UITGRLEVERD = 'uitgeleverd', 'Uitgeleverd'
        GRANNULEERD = 'geannuleerd', 'Geannuleerd'

    klant = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='recepten')
    arts_naam = models.CharField(max_length=200)
    arts_telefoon = models.CharField(max_length=20)
    datum = models.DateField()
    notities = models.TextField()
    aangemaakt_op = models.DateTimeField(auto_now_add=True)
    bijgewerkt_op = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NIEUW)

    def __str__(self):
        return f"Recept {self.pk} — {self.klant.username} — ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Recept'
        verbose_name_plural = 'Recepten'
        ordering = ['-aangemaakt_op']


class PrescriptionItem(models.Model):
    recept = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='Regels')
    medicijn = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    hoeveelheid = models.PositiveIntegerField()
    instructies = models.TextField(blank=True) # bijv. 2x per dag na het eten

    def __str__(self):
        return f"{self.hoeveelheid}x {self.medicijn} (Recept #{self.recept.pk})"

    class Meta:
        verbose_name = 'Receptregel'

