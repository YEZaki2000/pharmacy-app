from rest_framework import serializers
from .models import Category, Supplier, Medicine


# Category model serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'naam']


# Supplier model serializer
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'naam', 'contactpersoon', 'email', 'telefoon']


# Medicine model serializer
class MedicineSerializer(serializers.ModelSerializer):
    categorie_naam = serializers.CharField(source='categorie.naam', read_only=True)
    leverancier_naam = serializers.CharField(source='leverancier.naam', read_only=True)
    voorraad_laag = serializers.BooleanField(read_only=True)

    class Meta:
        model = Medicine
        fields = [
            'id',
            'naam',
            'dosering',
            'categorie',
            'categorie_naam',
            'leverancier',
            'leverancier_naam',
            'voorraad',
            'voorraad_laag',
            'minimum_voorraad',
            'omschrijving',
            'prijs',
            'vereist_recept'
        ]
        read_only_fields = ['aangemaakt_op', 'bijgewerkt_op']

        def validate_voorraad(self, value):
            """Zorg dat voorraad niet negatief kan zijn"""
            if value < 0:
                raise serializers.ValidationError("Voorraad kan niet negatief zijn")
            return value
