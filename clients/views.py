from rest_framework import viewsets
from .models import Client, Ticket,RelatedConsignee,ClientDocuments
from .serializers import ClientSerializer, TicketSerializer,RelatedConsigneeSerializer,ClientDocsSerializer
from rest_framework_bulk.generics import BulkModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


class ClientViewSet(BulkModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active','type','payment_terms']

class TicketViewSet(BulkModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active','client','status','priority']


class RelatedConsigneeViewSets(BulkModelViewSet):
    queryset=RelatedConsignee.objects.all()
    serializer_class=RelatedConsigneeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client']

class ClientDocseViewSets(BulkModelViewSet):
    queryset=ClientDocuments.objects.all()
    serializer_class=ClientDocsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active','client']
