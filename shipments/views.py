from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import views
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import (
    Shipment, ShipmentParty, ShipmentPackages, Transit, 
    PrePostLeg, RelatedDocuments, PickupDelivery, ShipmentCharges,Driver,Fleet
)
from .serializers import (
    ShipmentSerializer, ShipmentPartySerializer, ShipmentPackagesSerializer,
    TransitSerializer, PrePostLegSerializer, RelatedDocumentsSerializer,
    PickupDeliverySerializer, ShipmentChargesSerializer,DriverSerializer,FleetSerializer
)
from rest_framework_bulk.generics import BulkModelViewSet

class ShipmentViewSet(BulkModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    @action(detail=True, methods=['get'])
    def packages(self, request, pk=None):
        shipment = self.get_object()
        packages = ShipmentPackages.objects.filter(shipment=shipment)
        serializer = ShipmentPackagesSerializer(packages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def charges(self, request, pk=None):
        shipment = self.get_object()
        charges = ShipmentCharges.objects.filter(shipment=shipment)
        serializer = ShipmentChargesSerializer(charges, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        shipment = self.get_object()
        documents = RelatedDocuments.objects.filter(shipment=shipment)
        serializer = RelatedDocumentsSerializer(documents, many=True)
        return Response(serializer.data)

class ShipmentPartyViewSet(BulkModelViewSet):
    queryset = ShipmentParty.objects.all()
    serializer_class = ShipmentPartySerializer

    def get_queryset(self):
        queryset = ShipmentParty.objects.all()
        shipment_id = self.request.query_params.get('shipment', None)
        if shipment_id is not None:
            queryset = queryset.filter(shipment_id=shipment_id)
        return queryset

class ShipmentPackagesViewSet(BulkModelViewSet):
    queryset = ShipmentPackages.objects.all()
    serializer_class = ShipmentPackagesSerializer

    def get_queryset(self):
        queryset = ShipmentPackages.objects.all()
        shipment_id = self.request.query_params.get('shipment', None)
        if shipment_id is not None:
            queryset = queryset.filter(shipment_id=shipment_id)
        return queryset

class TransitViewSet(BulkModelViewSet):
    queryset = Transit.objects.all()
    serializer_class = TransitSerializer

    @action(detail=True, methods=['get'])
    def legs(self, request, pk=None):
        transit = self.get_object()
        legs = PrePostLeg.objects.filter(transit=transit)
        serializer = PrePostLegSerializer(legs, many=True)
        return Response(serializer.data)

class PrePostLegViewSet(BulkModelViewSet):
    queryset = PrePostLeg.objects.all()
    serializer_class = PrePostLegSerializer

class RelatedDocumentsViewSet(BulkModelViewSet):
    queryset = RelatedDocuments.objects.all()
    serializer_class = RelatedDocumentsSerializer

class PickupDeliveryViewSet(BulkModelViewSet):
    queryset = PickupDelivery.objects.all()
    serializer_class = PickupDeliverySerializer

class ShipmentChargesViewSet(BulkModelViewSet):
    queryset = ShipmentCharges.objects.all()
    serializer_class = ShipmentChargesSerializer

class DriverViewSet(BulkModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class FleetViewSet(BulkModelViewSet):
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer

class AddChargeToShipments(APIView):
    """
    API View to add a single charge to multiple shipments in bulk.
    """
    

    def post(self, request, *args, **kwargs):
        """
        Add a single charge to multiple shipments.
        
        Expected Request Body:
        {
            "charge": {
                "description": "Sample Charge",
                "amount": 100.0,
                "currency": 1  # Foreign key to currency model
            },
            "shipments": [1, 2, 3]  # List of shipment IDs
        }
        """
        charge_data = request.data.get("charge")
        shipment_ids = request.data.get("shipments")

        if not charge_data or not shipment_ids:
            return Response(
                {"error": "Both 'charge' and 'shipments' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate shipment IDs
        shipments = Shipment.objects.filter(id__in=shipment_ids)
        if not shipments.exists():
            return Response(
                {"error": "No valid shipments found for the provided IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add the charge to each shipment
        charge_objects = []
        for shipment in shipments:
            charge = ShipmentCharges(
                shipment=shipment,
                description=charge_data.get("description"),
                amount=charge_data.get("amount"),
                currency_id=charge_data.get("currency"),  # Assume currency is sent as ID
                user_add=request.user
            )
            charge_objects.append(charge)

        # Bulk create charges
        ShipmentCharges.objects.bulk_create(charge_objects)

        # Serialize and return the created charges
        serializer = ShipmentChargesSerializer(charge_objects, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)