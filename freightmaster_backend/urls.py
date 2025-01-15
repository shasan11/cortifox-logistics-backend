from django.contrib import admin
from django.urls import path,include
 
from rest_framework import permissions

urlpatterns = [
    path('auth/',include("djoser.urls")),
    path('auth/',include("djoser.urls.jwt")),
    path('cms/', admin.site.urls),
    path('general-accounting/',include('accounting.urls')),
    path('parties/',include('actor.urls')),
    path('clients/',include('clients.urls')),
    path('core/',include('core.urls')),
    path('crm/',include('crm.urls')),
    path('inventory/',include('inventory.urls')),
    path('master/',include('master.urls')),
    path('purchase/',include('purchase.urls')),
    path('sales/',include('sales.urls')),
    path('shipments/',include('shipments.urls')),
    path('warehouse/',include('warehouse.urls')),
    path('docs-generator/',include('docsprovider.urls')),
    
]
