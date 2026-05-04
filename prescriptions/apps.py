from django.apps import AppConfig


class PrescriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prescriptions'

    def ready(self):
        """
        Deze functie draait wanneed Django start.
        Hier laden we de signals.
        """
        import prescriptions.signals
