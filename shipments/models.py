from django.db import models
import uuid
from accounting.models import Currency
from master.models import UnitofMeasurement, UnitofMeasurementLength
from master import *
from master.models import PackageType
from master.models import *
from clients.models import Client
from master.models import Ports
from django.contrib.auth.models import User
from actor.models import Vendor
from core.getCurrentUser import get_current_user
from decimal import Decimal
from clients.models import Client, RelatedConsignee
from simple_history.models import HistoricalRecords

STATUS_CHOICES = (
    ('Draft', 'Draft'),
    ('Quotation', 'Quotation'),
    ('Booking', 'Booking'),
    ('Accepted', 'Accepted'),
    ('Pending', 'Pending'),
    ('Picked up', 'Picked up'),
    ('On Hold', 'On Hold'),
    ('Out for delivery', 'Out for delivery'),
    ('In Transit', 'In Transit'),
    ('Enroute', 'Enroute'),
    ('Cancelled', 'Cancelled'),
    ('Delivered', 'Delivered'),
    ('Returned', 'Returned'),
)

SHIPMENT_TYPE = [
    ("Direct", "Direct"),
    ("Booking", "Booking"),
    ("Master", "Master"),
    ("Consolidation", "Consolidation"),
]

SERVICE_TYPE = (
    ("FCL", "FCL"),
    ("LCL", "LCL")
) 

CHARGES_TYPES_ADMIN = (
    ("FIXED", "Fixed"),
    ("PP", "Per Package"),
    ("PV", "Per Unit Volume")
)

TRANSPORT_MEDIUM = (
    ("AIR", "AIR"),
    ("SEA", "SEA"),
    ("LAND", "Land"),
)

DELIVERY_CHOICES = (
    ("Import", "Import"),
    ("Export", "Export"),
    ("Domestic", "Transport")
)

TRANSPORTATION_TYPE = [
        ('Main Transportation', 'General Cargo'),
        ('Pre Transportation', 'Fragile Goods'),
        ('Post Transportation', 'Perishable Goods'),
    ]

PAYMENT_CHOICES = [
    ('prepaid', 'Prepaid'),
    ('collect', 'Collect'),
    ('third_party_billing', 'Third Party Billing'),
    ('freight_prepaid_and_add', 'Freight Prepaid and Add'),
    ('cod', 'Cash on Delivery'),
    ('credit_account', 'Credit Account'),
    ('eft', 'Electronic Funds Transfer'),
]

MOVEMENT_TYPE_CHOICES = [
        ('GR', 'Goods Receipt'),
        ('GI', 'Goods Issue'),
        ('TR', 'Transfer Posting'),
        ('ST', 'Stock Transfer'),
        ('RD', 'Return Delivery'),
        ('ID', 'Inbound Delivery'),
        ('OD', 'Outbound Delivery'),
        ('SM', 'Special Stock Movement'),
        # Add more as needed
    ]
def generate_custom_uuid():
    last_shipment = Shipment.objects.all().order_by('-id').first()
    last_shipment_id = last_shipment.id if last_shipment else 0
    unique_number = last_shipment_id + 300

    return f"SE-{unique_number:08d}"

def generate_custom_si():
    last_shipment = Shipment.objects.all().order_by('-id').first()
    last_shipment_id = last_shipment.id if last_shipment else 0
    unique_number = last_shipment_id + 500

    return f"SI-{unique_number:08d}"

def generate_custom_package_np():
    last_shipment = ShipmentPackages.objects.all().order_by('-id').first()
    last_shipment_id = last_shipment.id if last_shipment else 0
    unique_number = last_shipment_id + 5500

    return f"PKG-{unique_number:08d}"

class Shipment(models.Model):
    id = models.BigAutoField(primary_key=True)  
    uuid=models.CharField(default=uuid.uuid4,unique=True,max_length=120)
    shipment_no = models.CharField(max_length=50, verbose_name="Shipment Number", default=generate_custom_uuid)
    #GENERAL DETAILS
    si_no=models.CharField(default=generate_custom_si,max_length=100)
    shipment_type = models.CharField(choices=SHIPMENT_TYPE, max_length=50, default="Booking")
    is_roro = models.BooleanField(default=False)
    is_third_party = models.BooleanField(default=False)
    movement_type = models.CharField(max_length=2, choices=MOVEMENT_TYPE_CHOICES)    
    transport_mode = models.CharField(choices=TRANSPORT_MEDIUM, max_length=50)
    service_type = models.CharField(choices=SERVICE_TYPE, max_length=50)
    direction = models.CharField(choices=DELIVERY_CHOICES, max_length=50)
    shipment_status = models.CharField(max_length=50, default="Booking", blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name="Company Division", blank=True, null=True, related_name="shipments_branch")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Client", related_name="shipments_as_client", blank=True, null=True)
    inco_terms = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=100, choices=(("High", "High"), ("Low", "Low"), ("Medium", ("Medium"))))
    consignee = models.ForeignKey(RelatedConsignee, on_delete=models.PROTECT, related_name="consignees_related_shipment",blank=True,null=True)
    shipper= models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="shipper", blank=True, null=True)
    complementary=models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="shipments_currency")
    total_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(default=0, blank=True, null=True) 
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='prepaid', blank=True, null=True)
   
    customs_value = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    freight_value = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    insurance_value = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    invoice_value = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)

    
    # Extras
    is_client_approved=models.BooleanField(default=False)
    has_warehouse_jobs=models.BooleanField(default=False)
    invoices = models.BooleanField(default=False)
    is_dangerous_goods = models.BooleanField(default=False)
    is_damaged_goods = models.BooleanField(default=False)
    packaging_list = models.BooleanField(default=False)
    imo_number = models.CharField(blank=True, null=True, max_length=100)
    final_address = models.CharField(blank=True, null=True, max_length=100)
    order_no = models.CharField(blank=True, null=True, max_length=100)
    delivery_type = models.CharField(blank=True, null=True, max_length=100)
    doc_ref_no = models.CharField(blank=True, null=True, max_length=100)
    declaration_no = models.CharField(blank=True, null=True, max_length=100)
    order_no = models.CharField(blank=True, null=True, max_length=100)


    #Some Other
    origin_custom_clearance=models.BooleanField(default=False)
    destination_custom_clearance=models.BooleanField(default=False)
    open_financially=models.BooleanField(default=True)
    open_operationally=models.BooleanField(default=True)
    manifest_si_no=models.CharField(max_length=120,blank=True,null=True)

    
    # Date And Time
    scheduled_start_date = models.DateField(blank=True, null=True)
    scheduled_start_time = models.TimeField(blank=True, null=True)
    scheduled_end_date = models.DateField(blank=True, null=True)
    scheduled_end_time = models.TimeField(blank=True, null=True)
    
    # Port origin info
    port_origin = models.ForeignKey(Ports, on_delete=models.PROTECT, related_name="shipments_port_origin")
    port_handling_agent_origin = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="shipments_port_handling_agent_origin")
    eta_origin = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Arrival")
    etd_origin = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Departure")
    

    # Port destination info
    port_destination = models.ForeignKey(Ports, on_delete=models.PROTECT, related_name="shipments_port_destination")
    port_handling_agent_destination = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="shipments_port_handling_agent_destination")
    eta_origin_destination = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Arrival")
    etd_destination = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Departure")
    consignee = models.ForeignKey(RelatedConsignee, on_delete=models.PROTECT, related_name="consignees_related_shipment",blank=True,null=True)
    notify_party = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="notify_party", blank=True, null=True)

    # System default information
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="shipments_user_add")
    active = models.BooleanField(default=True)    
    history = HistoricalRecords() 

    #Booking Shipment Specifice Field
    master= models.ForeignKey('self', related_name="subshipments", blank=True,null=True,on_delete=models.CASCADE)
    is_loaded=models.BooleanField(default=False)
    booking_status=models.CharField(max_length=100,blank=True,null=True)   
    additionalInfo=models.TextField(blank=True,null=True) 



     # Air freight specific
    awb = models.CharField(max_length=50, blank=True, null=True)
    flight_number = models.CharField(max_length=50, blank=True, null=True)
    cargo_terminal = models.CharField(max_length=50, blank=True, null=True)
    handling_code = models.CharField(max_length=50, blank=True, null=True)   
    uld_no = models.CharField(max_length=50, blank=True, null=True)
    
    
    # Sea freight specific
    bol = models.CharField(max_length=50, blank=True, null=True)
    vessel_name = models.CharField(max_length=50, blank=True, null=True)
    voyage_number = models.CharField(max_length=50, blank=True, null=True)
    container_number = models.CharField(max_length=50, blank=True, null=True)
    container_type = models.CharField(max_length=50, blank=True, null=True)
     
    # Land freight specific 
    bol_land = models.CharField(max_length=50, blank=True, null=True)
    vehicle_number = models.CharField(max_length=50, blank=True, null=True)
    driver_info = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    cargo_type = models.CharField(max_length=50, blank=True, null=True,)
    trailer_type = models.CharField(max_length=50, blank=True, null=True,)
    handling_info=models.TextField(blank=True,null=True)
 

    class Meta:
        verbose_name_plural = "Shipments"

    def __str__(self):
        return str(self.shipment_no)  


class ShipmentParty(models.Model):
    id = models.BigAutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="shipment_party")
    type=models.CharField(max_length=100,choices=(
        ("Notify Party","Notify Party"),
        ("Exporter","Exporter"),
        ("Importer","Importer"),
        ("Notify Party Exporter","Notify Party Exporter"),
        ("Notify Party Importer","Notify Party Importer"),
        ("Forwarding","Forwarding"),
        ("Executed By","Executed By"),
        ))
    name = models.CharField(max_length=255,)
    phone = models.CharField(max_length=20,)
    email = models.EmailField()
    address = models.TextField()

   
class ShipmentPackages(models.Model):
    id = models.BigAutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="shipment_packages")
    shipment_package = models.CharField(max_length=50, verbose_name="Shipment Number", default=generate_custom_package_np)
    good_desc = models.CharField(max_length=50, null=True, blank=True, verbose_name="Good Desc")
    hs_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="HS Code")
    package_type = models.ForeignKey(PackageType, on_delete=models.PROTECT, related_name="pkg_type", verbose_name="Package Type", blank=True, null=True)
    length = models.FloatField(verbose_name="Length")
    width = models.FloatField(verbose_name="Width")
    height = models.FloatField(verbose_name="Height")
    package_unit = models.ForeignKey(UnitofMeasurementLength, on_delete=models.PROTECT, verbose_name="Unit of Length", related_name="pkg_unit_length")
    gross_weight = models.FloatField(verbose_name="Gross Weight", blank=True, null=True)
    mass_unit = models.ForeignKey(UnitofMeasurement, on_delete=models.PROTECT, verbose_name="Unit of Mass/Weight", related_name="pkg_unit_mass", blank=True, null=True)
    quantity = models.PositiveBigIntegerField(default=1, verbose_name="Quantity")
    updated = models.DateTimeField(auto_now=True)
    user_add_package = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="shipment_packages_user_add")
    active = models.BooleanField(default=True)
    volumetric_weight = models.FloatField(verbose_name="Volumetric Weight", blank=True, null=True, default=0)
    chargable = models.FloatField(blank=True, null=True, default=0)
    remarks=models.TextField(blank=True,null=True)
    class Meta:
        verbose_name = "Consignment / Packages"
        verbose_name_plural = "Consignment / Packages"

    def __str__(self):
            return str(self.good_desc) 

        
class Transit(models.Model):
    id = models.BigAutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="transits")
    transport_mode = models.CharField(choices=TRANSPORT_MEDIUM, max_length=50)
    poa = models.ForeignKey(Ports, on_delete=models.PROTECT, related_name="transit_poa")
    pod = models.ForeignKey(Ports, on_delete=models.PROTECT, related_name="transit_pod")
    tracking_no=models.CharField(max_length=100,null=True,blank=True)
    port_handling_agent = models.ForeignKey(User, on_delete=models.PROTECT, related_name="transits_port_handling_agent")
    eta = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Arrival")
    etd = models.DateField(null=True, blank=True, verbose_name="Estimated Time of Departure")
    remarks = models.TextField(blank=True, null=True)
    expected_start_date = models.DateTimeField(blank=True, null=True)
    expected_end_date = models.DateField(blank=True, null=True)
    actual_start_date = models.DateTimeField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)

    # Air freight specific
    awb = models.CharField(max_length=50, blank=True, null=True)
    flight_number = models.CharField(max_length=50, blank=True, null=True)
    cargo_terminal = models.CharField(max_length=50, blank=True, null=True)
    handling_code = models.CharField(max_length=50, blank=True, null=True)   
    uld_no = models.CharField(max_length=50, blank=True, null=True)
    
    
    # Sea freight specific
    bol = models.CharField(max_length=50, blank=True, null=True)
    vessel_name = models.CharField(max_length=50, blank=True, null=True)
    voyage_number = models.CharField(max_length=50, blank=True, null=True)
    container_number = models.CharField(max_length=50, blank=True, null=True)
    container_type = models.CharField(max_length=50, blank=True, null=True)
     
    # Land freight specific 
    bol_land = models.CharField(max_length=50, blank=True, null=True)
    vehicle_number = models.CharField(max_length=50, blank=True, null=True)
    driver_info = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    cargo_type = models.CharField(max_length=50, blank=True, null=True,)
    trailer_type = models.CharField(max_length=50, blank=True, null=True,)
    handling_info=models.TextField(blank=True,null=True)

    
    status = models.CharField(max_length=50, default="On Hold")
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    history = HistoricalRecords() 

class PrePostLeg(models.Model):
    id = models.BigAutoField(primary_key=True)
    transit=models.ForeignKey(Transit,on_delete=models.CASCADE,related_name="transit_post_pre_leg")
    type_leg = models.CharField(
    choices=[ ("PreLeg", "Pre Leg"), ("PostLeg", "Post Leg") ], max_length=100 ) 
    main_location=models.TextField()
    cargo_ready_date=models.DateField()
    pick_deliver_date=models.DateField()
    remarks=models.TextField()
    status=models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="shipments_user_add_post_pre")
    active = models.BooleanField(default=True) 
    history = HistoricalRecords()    

class RelatedDocuments(models.Model):
    id = models.BigAutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="documents")
    document_name = models.CharField(max_length=50, verbose_name="Document Name")
    document_no = models.CharField(max_length=50, verbose_name="Document Id/Code", null=True, blank=True)
    file = models.FileField(upload_to='documents/%Y-%m-%d')
    description = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="shipments_user_add_docs")
    active = models.BooleanField(default=True,editable=False)
    history = HistoricalRecords() 

    def __str__(self):
        return self.document_name

    class Meta:
        verbose_name = "Documents"
        verbose_name_plural = "Documents"


class Driver(models.Model):
    contact_person = models.CharField(max_length=50, verbose_name="Contact Person")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    email = models.EmailField(max_length=100, verbose_name="Email Address")
    address1 = models.TextField(verbose_name="Address 1")
    address2 = models.TextField(blank=True, null=True, verbose_name="Address 2")
    license_number = models.CharField(max_length=20, verbose_name="Driver License Number", blank=True, null=True)
    vehicle_type = models.CharField(max_length=50, verbose_name="Preferred Vehicle Type", blank=True, null=True)
    emergency_contact = models.CharField(max_length=50, verbose_name="Emergency Contact", blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=(("Active", "Active"), ("Inactive", "Inactive"), ("Suspended", "Suspended")), 
        default="Active", 
        verbose_name="Driver Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date Updated")
    
    def __str__(self):
        return self.contact_person


class Fleet(models.Model):
    vehicle_name = models.CharField(max_length=50, verbose_name="Vehicle Name")
    vehicle_type = models.CharField(max_length=50, verbose_name="Vehicle Type")  # e.g., truck, van, etc.
    license_plate = models.CharField(max_length=15, verbose_name="License Plate Number")
    capacity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Capacity (in tons)")
    owner_name = models.CharField(max_length=100, verbose_name="Owner Name", blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=(("Available", "Available"), ("In Transit", "In Transit"), ("Under Maintenance", "Under Maintenance")),
        default="Available",
        verbose_name="Fleet Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date Updated")
    
    def __str__(self):
        return f"{self.vehicle_name} - {self.license_plate}"


class PickupDelivery(models.Model):
    id = models.BigAutoField(primary_key=True)
    shipment = models.ForeignKey("Shipment", on_delete=models.CASCADE, related_name="shipment_pickup_delivery")
    type_leg = models.CharField(
        choices=(("Pickup", "Pickup"), ("Delivery", "Delivery")), 
        max_length=100, 
        verbose_name="Leg Type"
    )
    main_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="Main Type (e.g., express, regular)")
    expected_pickup_date = models.DateField(verbose_name="Expected Pickup Date")
    expected_pickup_time = models.TimeField(verbose_name="Expected Pickup Time")
    actual_pickup_date = models.DateField(null=True, blank=True, verbose_name="Actual Pickup Date")
    actual_pickup_time = models.TimeField(null=True, blank=True, verbose_name="Actual Pickup Time")
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name="pickup_delivery_driver")
    fleet = models.ForeignKey(Fleet, on_delete=models.PROTECT, related_name="pickup_delivery_vehicle")
    status = models.CharField(
        max_length=100,
        choices=(("Pending", "Pending"), ("In Progress", "In Progress"), ("Completed", "Completed"), ("Failed", "Failed")),
        default="Pending",
        verbose_name="Status"
    )
    pod = models.FileField(upload_to="proof-of-delivery", blank=True, null=True, verbose_name="Proof of Delivery (POD)")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    user_add = models.ForeignKey(
        User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="pc_user_pickup_delivery"
    )
    active = models.BooleanField(default=True, verbose_name="Active Status")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.shipment} - {self.type_leg} - {self.status}"

class ShipmentCharges(models.Model):
    id = models.BigAutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="shipment_charges")
    charge_name = models.TextField(max_length=50)
    charge_type = models.CharField(max_length=50, default="Fixed", editable=False)
    rate = models.FloatField()
    qty = models.FloatField()
    total = models.FloatField()
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, related_name="shipment_charges_add")
    active = models.BooleanField(default=True, editable=False)
    history = HistoricalRecords() 

    class Meta:
        verbose_name = "Charges"
        verbose_name_plural = "Charges"



 