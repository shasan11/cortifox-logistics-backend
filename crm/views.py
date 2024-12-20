from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ContactsGroup, Contacts, Deal, LeadsActivity, LeadsDocs
from .serializers import ContactsGroupSerializer, ContactsSerializer, DealSerializer, LeadsActivitySerializer, LeadsDocsSerializer
from rest_framework_bulk.generics import BulkModelViewSet
class ContactsGroupViewSet(BulkModelViewSet):
    queryset = ContactsGroup.objects.all()
    serializer_class = ContactsGroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['uuid', 'active', 'user_add']  # Filters by UUID, active status, and user who added it
    search_fields = ['name', 'description']  # Search by name or description
    ordering_fields = ['created', 'updated']  # Order by created or updated dates


class ContactsViewSet(BulkModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['uuid', 'active', 'user_add', 'contact_group']  # Filters by UUID, active status, user who added, and contact group
    search_fields = ['name', 'phone', 'email', 'PAN', 'address']  # Search by contact fields
    ordering_fields = ['created', 'updated']  # Order by created or updated dates


class DealViewSet(BulkModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['uuid', 'active', 'user_add', 'deals_stage', 'deal_contact', 'assign_to']  # Filters by UUID, active status, user who added, deal stage, contact, and assigned user
    search_fields = ['title', 'description']  # Search by title or description
    ordering_fields = ['created', 'updated', 'expected_closing_date', 'expected_revenue']  # Order by created, updated dates, expected closing date, or revenue


class LeadsActivityViewSet(BulkModelViewSet):
    queryset = LeadsActivity.objects.all()
    serializer_class = LeadsActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['uuid', 'active', 'user_add', 'deal', 'activity_type', 'performed_by']  # Filters by UUID, active status, user who added, deal, activity type, and performer
    search_fields = ['activity_type', 'description']  # Search by activity type or description
    ordering_fields = ['created', 'updated', 'date']  # Order by created, updated, or activity date


class LeadsDocsViewSet(BulkModelViewSet):
    queryset = LeadsDocs.objects.all()
    serializer_class = LeadsDocsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['uuid', 'active', 'user_add', 'deal', 'uploaded_by']  # Filters by UUID, active status, user who added, deal, and uploader
    search_fields = ['document_name']  # Search by document name
    ordering_fields = ['created', 'updated', 'upload_date']  # Order by created, updated, or upload date
