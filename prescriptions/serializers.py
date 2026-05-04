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
