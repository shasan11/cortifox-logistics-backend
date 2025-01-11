from rest_framework import serializers
from django.contrib.auth.models import User
from shipments.models import (
    Shipment, ShipmentParty, ShipmentPackages, Transit, PrePostLeg,
    RelatedDocuments, Driver
)

# Custom User Serializer to exclude sensitive fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Include only the required fields

class DriverSerializer(serializers.ModelSerializer):
    user_add = UserSerializer(read_only=True)  # Use the custom UserSerializer

    class Meta:
        model = Driver
        fields = "__all__"

class ShipmentPackagesSerializer(serializers.ModelSerializer):
    user_add = UserSerializer(read_only=True)

    class Meta:
        model = ShipmentPackages
        fields = "__all__"

class ShipmentPartySerializer(serializers.ModelSerializer):
    user_add = UserSerializer(read_only=True)

    class Meta:
        model = ShipmentParty
        fields = "__all__"

class RelatedDocumentsSerializer(serializers.ModelSerializer):
    user_add = UserSerializer(read_only=True)

    class Meta:
        model = RelatedDocuments
        fields = "__all__"

class TransitSerializer(serializers.ModelSerializer):
    user_add = UserSerializer(read_only=True)

    class Meta:
        model = Transit
        fields = "__all__"

class PrePostLegSerializer(serializers.ModelSerializer):
    user_add = UserSerializer(read_only=True)

    class Meta:
        model = PrePostLeg
        fields = "__all__"

class ShipmentSerializer(serializers.ModelSerializer):
    shipment_party = ShipmentPartySerializer(many=True, read_only=True)
    shipment_packages = ShipmentPackagesSerializer(many=True, read_only=True)
    transits = TransitSerializer(many=True, read_only=True)
    documents = RelatedDocumentsSerializer(many=True, read_only=True)
    driver = DriverSerializer(read_only=True)  # Use the custom DriverSerializer
    user_add = UserSerializer(read_only=True)  # Serialize user_add explicitly

    class Meta:
        model = Shipment
        fields = "__all__"
        depth=2
