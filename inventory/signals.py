from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Medicine


@receiver(pre_save, sender=Medicine)
def check_voorraad_wijziging(sender, instance, **kwargs):
    """
    Check of de voorraad handmatig is gewijzigd
    en log dit.
    """
    if instance.pk:  # Als het een bestaand object is (niet nieuw)
        try:
            oude_medicine = Medicine.objects.get(pk=instance.pk)
            
            if oude_medicine.voorraad != instance.voorraad:
                verschil = instance.voorraad - oude_medicine.voorraad
                
                if verschil > 0:
                    print(f"📦 Voorraad toegevoegd: {instance.naam} +{verschil} stuks")
                else:
                    print(f"📉 Voorraad verwijderd: {instance.naam} {verschil} stuks")
        except Medicine.DoesNotExist:
            pass
