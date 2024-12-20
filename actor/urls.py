from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from . import views

router = BulkRouter()
router.register(r'vendors', views.VendorViewSet)  # Removed trailing slash

urlpatterns = [
    path('', include(router.urls)),
]
