from rest_framework import serializers
from .models import CryptoAddress

# Serializer for the CryptoAddress model
class CryptoAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAddress
        fields = '__all__'

