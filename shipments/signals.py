from django.db.models.signals import pre_save, post_save,post_delete,pre_delete
from django.dispatch import receiver
from django.db import transaction
from .models import ShipmentPackages
from warehouse.models import ShipmentItems
from decimal import Decimal
from django.db import models



@receiver(post_save, sender=ShipmentPackages)
def create_or_update_shipment_items(sender, instance, **kwargs):
    """
    Create or update shipment items based on the quantity of shipment packages.
    Adds new items if quantity increases, removes excess items if quantity decreases.
    """
    shipment = instance.shipment
    package = instance
    quantity = package.quantity

    # Fetch existing shipment items for this package
    existing_items = ShipmentItems.objects.filter(
        shipment=shipment, shipment_package__id=package.id
    ).distinct().order_by('package_no')

    if existing_items.count() < quantity:
        # Add new items if quantity increased
        for i in range(existing_items.count() + 1, quantity + 1):
            new_item = ShipmentItems.objects.create(
                shipment=shipment,
                package_no=f"SE{shipment.id}_{i}"
            )
            # Add the package to the ManyToManyField
            new_item.shipment_package.add(package)

    elif existing_items.count() > quantity:
        # Remove excess items if quantity decreased
        excess_items = existing_items[quantity:]
        for item in excess_items:
            item.delete()




@receiver(pre_delete, sender=ShipmentPackages)
def delete_shipment_items(sender, instance, **kwargs):
    """
    Delete all shipment items when a shipment package is deleted.
    """
    ShipmentItems.objects.filter(shipment_package=instance).delete()