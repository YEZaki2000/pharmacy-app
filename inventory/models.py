from django.db import models

# Create your models here.


# Categorie Model
class Category(models.Model):
    naam = models.CharField(max_length=100)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Categoriëen'


# Leverancier Model
class Supplier(models.Model):
    naam = models.CharField(max_length=200)
    contactpersoon = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    telefoon = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name = 'Leverancier'


# Medecijn Model
class Medicine(models.Model):
    naam = models.CharField(max_length=200)
    dosering = models.CharField(max_length=200) # bijv. 500mg
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    leverancier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    voorraad = models.PositiveIntegerField(default=0)
    minimum_voorraad = models.PositiveIntegerField(default=10) # voor waarschuwing
    prijs = models.DecimalField(max_digits=8, decimal_places=2)
    omschrijving = models.TextField(blank=True)
    aangemaakt_op = models.DateTimeField(auto_now_add=True)
    bijgewerkt_op = models.DateTimeField(auto_now=True)
    vereist_recept = models.BooleanField(default=False)

    @property
    def voorraad_laag(self):
        return self.voorraad <= self.minimum_voorraad

    def __str__(self):
        return f"{self.naam} {self.dosering}"

    class Meta:
        verbose_name = 'Medicijn'
        verbose_name_plural = 'Medicijnen'


