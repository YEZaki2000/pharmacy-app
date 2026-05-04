from rest_framework import serializers
from .models import CustomerProfile
from accounts.models import CustomUser

class CustomerProfileSerializer(serializers.ModelSerializer):
    naam = serializers.CharField(source='user.get_full_name()', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'user',
            'email',
            'naam',
            'username',
            'geboortedatum',
            'telefoon',
            'adres',
            'allergiëen',
            'aangemaakt_op'
        ]
        read_only_fields = ['user', 'aangemaakt_op']
        extra_kwargs = {
            'bsn': {'write_only': True}
        }
