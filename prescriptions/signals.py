from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PrescriptionItem
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=PrescriptionItem)
def verlaag_voorraad_bij_aanmaken(sender, instance, created, **kwargs):
    if created:
        medicijn = instance.medicijn
        
        # Verlaag voorraad
        oude_voorraad = medicijn.voorraad
        medicijn.voorraad -= instance.hoeveelheid
        
        if medicijn.voorraad < 0:
            medicijn.voorraad = 0
        
        medicijn.save()
        
        print(f"✅ Voorraad verlaagd: {medicijn.naam} {oude_voorraad} → {medicijn.voorraad}")
        
        # Stuur email als voorraad laag is
        if medicijn.voorraad_laag and oude_voorraad > medicijn.minimum_voorraad:
            # De voorraad is NU pas onder het minimum gekomen
            stuur_lage_voorraad_email(medicijn)


def stuur_lage_voorraad_email(medicijn):
    """
    Stuur een email naar de apotheker
    """
    onderwerp = f"⚠️ Lage voorraad: {medicijn.naam}"
    bericht = f"""
    De voorraad van {medicijn.naam} ({medicijn.dosering}) is laag!
    
    Huidige voorraad: {medicijn.voorraad} stuks
    Minimum voorraad: {medicijn.minimum_voorraad} stuks
    
    Gelieve nieuwe voorraad te bestellen.
    """
    
    # Voor nu alleen printen, later kun je echte email sturen
    print("=" * 50)
    print(f"📧 EMAIL VERZONDEN")
    print(f"Aan: apotheker@pharmacy.nl")
    print(f"Onderwerp: {onderwerp}")
    print(bericht)
    print("=" * 50)
    
    # Uncomment dit als je echte emails wilt sturen:
    # send_mail(
    #     subject=onderwerp,
    #     message=bericht,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=['apotheker@pharmacy.nl'],
    #     fail_silently=True,
    # )


@receiver(post_delete, sender=PrescriptionItem)
def verhoog_voorraad_bij_verwijderen(sender, instance, **kwargs):
    medicijn = instance.medicijn
    medicijn.voorraad += instance.hoeveelheid
    medicijn.save()
    
    print(f"↩️ Voorraad verhoogd: {medicijn.naam} nu {medicijn.voorraad} stuks")
