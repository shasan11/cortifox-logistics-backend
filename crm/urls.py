from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactsGroupViewSet, ContactsViewSet, DealViewSet, LeadsActivityViewSet, LeadsDocsViewSet
from rest_framework_bulk.routes import BulkRouter

# Create a router and register our viewsets with it.
router = BulkRouter()
router.register(r'contacts-groups', ContactsGroupViewSet, basename='contacts-group')
router.register(r'contacts', ContactsViewSet, basename='contacts')
router.register(r'deals', DealViewSet, basename='deal')
router.register(r'leads-activities', LeadsActivityViewSet, basename='leads-activity')
router.register(r'leads-docs', LeadsDocsViewSet, basename='leads-doc')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
