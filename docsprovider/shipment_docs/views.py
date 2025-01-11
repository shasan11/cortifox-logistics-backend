from rest_framework.generics import RetrieveAPIView
from shipments.models import Shipment
from .serializers import ShipmentSerializer

class ShipmentDetailView(RetrieveAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
