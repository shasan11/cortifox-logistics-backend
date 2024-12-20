from rest_framework_bulk.serializers import BulkSerializerMixin
from rest_framework import serializers
from .models import ContactsGroup, Contacts, Deal, LeadsActivity, LeadsDocs
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class ContactsGroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ContactsGroup
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer


class ContactsSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer


class DealSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer


class LeadsActivitySerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = LeadsActivity
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer



class LeadsDocsSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = LeadsDocs
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
