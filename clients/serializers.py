from rest_framework import serializers
from .models import Client, Ticket,ClientDocuments,RelatedConsignee
from rest_framework_bulk.serializers import BulkSerializerMixin
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class ClientSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = Client
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class ClientDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocuments
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
        
class RelatedConsigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedConsignee
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer               
        
        
