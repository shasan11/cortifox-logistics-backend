from django.db import models
import uuid
from django.contrib.auth.models import User
from core.getCurrentUser import get_current_user
from master.models import UnitofMeasurementLength,UnitofMeasurement
from shipments.models import Shipment,ShipmentPackages
from simple_history.models import HistoricalRecords
from master.models import Ports
from actor.models import Vendor

class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="Name")
    code = models.CharField(max_length=20, verbose_name="Code")
    type = models.CharField(choices=[('self', 'Self'), ('agent', 'Agent')], max_length=10, verbose_name="Type")
    contact_person = models.CharField(max_length=255, blank=True, null=True, verbose_name="Contact Person")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    note=models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="warehouse_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 

    def __str__(self):
        return self.name or str(self.uuid)
    
    class Meta:
        verbose_name_plural="Warehouse Master"
        
 


class WarehouseStorage(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='storages', verbose_name="Warehouse")
    name = models.CharField(max_length=255, verbose_name="Name")
    code = models.CharField(max_length=20, verbose_name="Code")
    temp = models.FloatField(verbose_name="Temperature")
    max_vol = models.FloatField(verbose_name="Max Volume")
    min_temp = models.FloatField(verbose_name="Min Temperature")
    max_temp = models.FloatField(verbose_name="Max Temperature")
    package_unit = models.ForeignKey(UnitofMeasurementLength, on_delete=models.PROTECT, verbose_name="Unit of Mass/Weight", related_name="pkg_unit_mass", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="warehouse_storage_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 

    def __str__(self):
        return self.name or str(self.uuid)
    
    class Meta:
        verbose_name_plural="Warehouse Storage"

class WarehouseBin(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    warehouse_storage = models.ForeignKey(WarehouseStorage, on_delete=models.CASCADE, related_name='bins', verbose_name="Warehouse Storage")
    client = models.CharField(max_length=255, verbose_name="Client")
    code = models.CharField(max_length=20, verbose_name="Code")
    name = models.CharField(max_length=255, verbose_name="Name")
    type = models.CharField(max_length=50, verbose_name="Type")
    barcode = models.CharField(max_length=50, blank=True, null=True, verbose_name="Barcode")
    check_digit = models.CharField(max_length=1, blank=True, null=True, verbose_name="Check Digit")
    max_vol = models.FloatField(verbose_name="Max Volume")
    max_gweight = models.FloatField(verbose_name="Max Gross Weight")
    max_nweight = models.FloatField(verbose_name="Max Net Weight")
    max_vweight = models.FloatField(verbose_name="Max Volumetric Weight")
    mass_unit = models.ForeignKey(UnitofMeasurement, on_delete=models.PROTECT, verbose_name="Unit of Mass/Weight", related_name="pkg_unit_mass_warehouse_bin_location_list", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="bin_location_list_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 

    def __str__(self):
        return self.name or str(self.uuid)
    
    class Meta:
        verbose_name_plural="Warehouse Bin"

class ShipmentItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="shipment_items")
    shipment_package = models.ManyToManyField(ShipmentPackages)
    package_no=models.CharField(max_length=100)
    container_no = models.CharField(max_length=50, default="Fixed", editable=False)
    seal_no = models.CharField(max_length=50, default="Fixed", editable=False)
    loading_point = models.CharField(max_length=50, default="Fixed", editable=False)
    pickup_point= models.CharField(max_length=50, default="Fixed", editable=False)
    warehouse= models.ForeignKey(WarehouseBin,null=True,blank=True,on_delete=models.PROTECT,related_name="Warehiouse_shipment_itmes")
    is_damaged = models.BooleanField(default=False, editable=False)
    is_missing = models.BooleanField(default=False, editable=False)
    status = models.CharField(max_length=50, default="On Hold")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="shipments_item_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 
    
def generate_asn_no():
    last_shipment = ASN.objects.all().order_by('-id').first()
    last_shipment_id = last_shipment.id if last_shipment else 0
    unique_number = last_shipment_id + 500

    return f"ASN-{unique_number:08d}"

def generate_grn_no():
    last_shipment = GoodsRecieptNote.objects.all().order_by('-id').first()
    last_shipment_id = last_shipment.id if last_shipment else 0
    unique_number = last_shipment_id + 500

    return f"GRN-{unique_number:08d}"

def generate_gio_uuid():
    last_shipment = GoodsIssueOrder.objects.all().order_by('-id').first()
    last_shipment_id = last_shipment.id if last_shipment else 0
    unique_number = last_shipment_id + 500

    return f"GIO-{unique_number:08d}"

def generate_gdn_uuid():
    last_shipment = GoodsDispatchOrder.objects.all().order_by('-id').first()
    last_shipment_id = last_shipment.id if last_shipment else 0
    unique_number = last_shipment_id + 500

    return f"GDN-{unique_number:08d}"

class WarehouseJobsOrders(models.Model):
    id = models.AutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='warehouse_orders_shipments', verbose_name="Shipment")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    warehouse_bin = models.ForeignKey(WarehouseBin, on_delete=models.CASCADE, related_name='warehouse_orders_warehouses_bin', verbose_name="Warehouse Bin")
    scheduled_start_date = models.DateField(blank=True, null=True)
    scheduled_start_time = models.TimeField(blank=True, null=True)
    scheduled_end_date = models.DateField(blank=True, null=True)
    scheduled_end_time = models.TimeField(blank=True, null=True)

    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_order_stock_transfers_from', verbose_name="From Warehouse")
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_order_stock_transfers_to', verbose_name="To Warehouse")
    from_warehouse_bin = models.ForeignKey(WarehouseBin, on_delete=models.CASCADE, related_name='warehouse_order_stock_transfers_from_bins', verbose_name="From Warehouse Bin")
    to_warehouse_bin = models.ForeignKey(WarehouseBin, on_delete=models.CASCADE, related_name='warehouse_order_stock_transfers_to_bins', verbose_name="To Warehouse Bin")
  
    port_origin = models.ForeignKey(Ports, on_delete=models.PROTECT, related_name="shipments_port_origin")
    port_handling_agent_origin = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="shipments_port_handling_agent_origin")
    eta_origin = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Arrival")
    etd_origin = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Departure")
    

    # Port destination info
    port_destination = models.ForeignKey(Ports, on_delete=models.PROTECT, related_name="shipments_port_destination")
    port_handling_agent_destination = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="shipments_port_handling_agent_destination")
    eta_origin_destination = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Arrival")
    etd_destination = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Departure")


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="warehouse_job_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 

    



class ASN(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    asn_no = models.CharField(max_length=50, verbose_name="ASN No.",default=generate_asn_no,)
    cleint_ref_no = models.CharField(max_length=50, verbose_name="Client Reference No.")
    boe_no = models.CharField(max_length=50, verbose_name="Client Reference No.",blank=True,null=True)
    cleint_ref_no = models.CharField(max_length=50, verbose_name="Client Reference No.")
    warehouse_orders=models.ForeignKey(WarehouseJobsOrders,on_delete=models.CASCADE,related_name="ASN_WAREHOUSE_ORDER")
    from_date = models.DateField(verbose_name="From Date")
    to_date = models.DateField(verbose_name="To Date")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    shipment = models.ForeignKey(ShipmentItems, on_delete=models.CASCADE, related_name='asns', verbose_name="Shipment")
    is_received = models.BooleanField(verbose_name="Is Received")
    is_issued = models.BooleanField(verbose_name="Is Issued")
    is_delivered = models.BooleanField(verbose_name="Is Delivered")
    desc=models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="asn_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 


    def __str__(self):
        return f"ASN {self.cleint_ref_no}"

    class Meta:
        verbose_name_plural="Advanced Shipping Note"


class GoodsRecieptNote(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    grn = models.CharField(max_length=50, verbose_name="GRN No.",default=generate_grn_no,)
    asn = models.ForeignKey(ASN, on_delete=models.CASCADE, related_name='grn_warehouses_asn', verbose_name="Warehouse")
    cleint_ref_no = models.CharField(max_length=50, verbose_name="Client Reference No.")
    boe_no = models.CharField(max_length=50, verbose_name="Client Reference No.",blank=True,null=True)
    warehouse_orders=models.ForeignKey(WarehouseJobsOrders,on_delete=models.CASCADE,related_name="GRN_WAREHOUSE_ORDER")
    cleint_ref_no = models.CharField(max_length=50, verbose_name="Client Reference No.")
    from_date = models.DateField(verbose_name="From Date")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    desc=models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="grn_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 


class GoodsIssueOrder(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    gio_no = models.CharField(max_length=50, verbose_name="GDO No.",default=generate_gio_uuid)
    date = models.DateField(verbose_name="From Date")
    warehouse_orders=models.ForeignKey(WarehouseJobsOrders,on_delete=models.CASCADE,related_name="GIO_WAREHOUSE_ORDER")
    client_desc=models.TextField(blank=True,null=True)
    ref_no_no = models.CharField(max_length=50, verbose_name="RefNo")
    client_ref_date = models.DateField(verbose_name="From Date",blank=True,null=True)
    eta = models.DateField(verbose_name="ETA",blank=True,null=True)
    etd = models.DateField(verbose_name="ETD",blank=True,null=True)
    picking_method=models.CharField(max_length=10,default="FIFO")
    remarks=models.TextField(blank=True,null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="gio_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 

class GoodsDispatchOrder(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    gdo_no = models.CharField(max_length=50, verbose_name="GDO No.",default=generate_gdn_uuid)
    date = models.DateField(verbose_name="Dispatch Date")
    warehouse_orders=models.ForeignKey(WarehouseJobsOrders,on_delete=models.CASCADE,related_name="GDO_WAREHOUSE_ORDER")  
    
    shipment = models.ForeignKey(ShipmentItems, on_delete=models.CASCADE, related_name='gdos_shipment_items', verbose_name="Shipment Items")
    client_ref_no = models.CharField(max_length=50, verbose_name="Client Reference No.")
    dispatch_method = models.CharField(max_length=50, verbose_name="Dispatch Method", default="Truck")
    delivery_address = models.TextField(verbose_name="Delivery Address", blank=True, null=True)
    carrier = models.CharField(max_length=100, verbose_name="Carrier", blank=True, null=True)
    eta = models.DateField(verbose_name="Estimated Time of Arrival", blank=True, null=True)
    etd = models.DateField(verbose_name="Estimated Time of Dispatch", blank=True, null=True)
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    is_dispatched = models.BooleanField(default=False, verbose_name="Is Dispatched")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="gdo_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 

    def __str__(self):
        return f"GDO {self.gdo_no} - {self.client_ref_no}"

    class Meta:
        verbose_name_plural = "Goods Dispatch Orders"


class StockTransfer(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    transfer_no = models.CharField(max_length=50, verbose_name="Transfer No.")
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_transfers_from', verbose_name="From Warehouse")
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_transfers_to', verbose_name="To Warehouse")
    from_warehouse_bin = models.ForeignKey(WarehouseBin, on_delete=models.CASCADE, related_name='stock_transfers_from_bins', verbose_name="From Warehouse Bin")
    to_warehouse_bin = models.ForeignKey(WarehouseBin, on_delete=models.CASCADE, related_name='stock_transfers_to_bins', verbose_name="To Warehouse Bin")
    shipmentitems = models.ForeignKey(ShipmentItems, on_delete=models.CASCADE, related_name='gdos', verbose_name="Shipment")
    transfer_date = models.DateField(verbose_name="Transfer Date")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    is_completed = models.BooleanField(verbose_name="Is Completed")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="stock_transfer_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 


    def __str__(self):
        return f"Stock Transfer {self.transfer_no}"
    
    class Meta:
        verbose_name_plural="Stock Transfer"

 