from .models import PrescriptionItem, Prescription
from rest_framework import serializers
from inventory.serializers import MedicineSerializer
from accounts.models import CustomUser



#PrescriptionItem serializer
class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicijn_naam = serializers.CharField(source='medicijn.naam', read_only=True)
    medicijn_dosering = serializers.CharField(source='medicijn.dosering', read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = [
            'id',
            'medicijn',
            'medicijn_naam',
            'medicijn_dosering',
            'hoeveelheid',
            'instructies',
        ]


class PrescriptionSerializer(serializers.ModelSerializer):
    regels = PrescriptionItemSerializer(many=True)
    klant_naam = serializers.CharField(source='klant.get_full_name', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'klant',
            'klant_naam',
            'arts_naam',
            'arts_telefoon',
            'datum',
            'notities',
            'status',
            'regels',
            'aangemaakt_op',
            'bijgewerkt_op'
        ]
        read_only_fields = ['aangemaakt_op', 'bijgewerkt_op']

    def validate_status(self, value):
        """
        Valideer dat statusovergangen logisch zijn
        """
        if not self.instance:  # Nieuw recept
            # Nieuwe recepten moeten status 'nieuw' hebben
            if value != Prescription.Status.NIEUW:
                raise serializers.ValidationError(
                    "Nieuwe recepten moeten status 'nieuw' hebben"
                )
            return value
        
        # Bij update: check oude status
        oude_status = self.instance.status
        
        # Geannuleerde recepten kunnen niet meer gewijzigd worden
        if oude_status == Prescription.Status.GEANNULEERD:
            raise serializers.ValidationError(
                "Een geannuleerd recept kan niet meer worden gewijzigd"
            )
        
        # Uitgeleverde recepten kunnen niet terug
        if oude_status == Prescription.Status.UITGELEVERD:
            if value != Prescription.Status.UITGELEVERD:
                raise serializers.ValidationError(
                    "Een uitgeleverd recept kan niet terug worden gezet"
                )
        
        # Geldige statusovergangen
        ALLOWED_TRANSITIONS = {
            Prescription.Status.NIEUW: [
                Prescription.Status.IN_BEHANDELING,
                Prescription.Status.GEANNULEERD
            ],
            Prescription.Status.IN_BEHANDELING: [
                Prescription.Status.KLAAR,
                Prescription.Status.GEANNULEERD
            ],
            Prescription.Status.KLAAR: [
                Prescription.Status.UITGELEVERD,
                Prescription.Status.GEANNULEERD
            ],
        }
        
        allowed = ALLOWED_TRANSITIONS.get(oude_status, [])
        if value != oude_status and value not in allowed:
            raise serializers.ValidationError(
                f"Overgang van '{oude_status}' naar '{value}' is niet toegestaan. "
                f"Toegestane statussen: {', '.join(allowed)}"
            )
        
        return value





class PrescriptionCreateSerializer(serializers.ModelSerializer):
    """
    Aparte serilaizer voor het aanmaken van recepten met regels
	"""
    regels = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = [
            'klant',
            'arts_naam',
            'arts_telefoon',
            'datum',
            'status',
            'notities',
            'regels'
        ]
    

    def create(self, validated_data):
        regels_data = validated_data.pop('regels')
        prescription = Prescription.objects.create(**validated_data)

        for regel_data in regels_data:
            PrescriptionItem.objects.create(recept=prescription, **regel_data)

        return prescription
