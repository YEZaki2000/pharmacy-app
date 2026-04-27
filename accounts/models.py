from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        PHARMACIST = 'pharmacist', 'Apotheker'
        CUSTOMER = 'customer', 'Klant'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    def is_pharmacist(self):
        return self.role == self.Role.PHARMACIST

    def __str__(self):
        return f"{self.username}, ({self.get_role_display()})"


