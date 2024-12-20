from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter
from . import views

router = BulkRouter()
router.register(r'clients', views.ClientViewSet)
#router.register(r'tickets', views.TicketViewSet)
router.register(r'consingee', views.RelatedConsigneeViewSets)
#router.register(r'docs', views.ClientDocseViewSets)

urlpatterns = [
    path('', include(router.urls)),
]

 