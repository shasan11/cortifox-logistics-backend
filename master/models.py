from django.db import models
from django.contrib.auth.models import User
from core.getCurrentUser import get_current_user
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError

class UnitofMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50, verbose_name="Unit Name")
    symbol = models.CharField(max_length=50, verbose_name="Unit Symbol")
    conversion_to_kg = models.DecimalField(verbose_name="Conversion to Kilogram", decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    add_by = models.ForeignKey(User, blank=True, null=True, default=get_current_user, on_delete=models.PROTECT, related_name="un_add")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Unit of Measurement"

    def __str__(self):
        return self.name

    def clean(self):
        if self.conversion_to_kg <= 0:
            raise ValidationError({"conversion_to_kg": "Conversion to Kilogram must be greater than 0."})


class UnitofMeasurementLength(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50, verbose_name="Unit Name")
    symbol = models.CharField(max_length=50, verbose_name="Unit Symbol")
    conversion_to_cm = models.DecimalField(verbose_name="Conversion to Centi Meters", decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    added_by = models.ForeignKey(User, blank=True, null=True, default=get_current_user, on_delete=models.PROTECT, related_name="unl_add")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Unit of Measurement (Length)"

    def __str__(self):
        return self.name

    def clean(self):
        if self.conversion_to_cm <= 0:
            raise ValidationError({"conversion_to_cm": "Conversion to Centi Meters must be greater than 0."})


class Ports(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50, verbose_name="Port Name")
    symbol = models.CharField(max_length=50, verbose_name="Port Symbol")
    active_status = models.BooleanField(default=True, verbose_name='Active')
    iso = models.CharField(max_length=50, verbose_name="ISO", blank=True, null=True)
    iata = models.CharField(max_length=50, verbose_name="IATA", blank=True, null=True)
    edi = models.CharField(max_length=50, verbose_name="EDI", blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name="Country", blank=True, null=True)
    region = models.CharField(max_length=50, verbose_name="Region", blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name="City", blank=True, null=True)
    is_land = models.BooleanField(default=True, verbose_name='Land')
    is_air = models.BooleanField(default=True, verbose_name='Air')
    is_sea = models.BooleanField(default=True, verbose_name='Sea')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    added_by = models.ForeignKey(User, blank=True, null=True, default=get_current_user, on_delete=models.PROTECT)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Ports"

    def __str__(self):
        return self.name

    def clean(self):
        if not any([self.is_land, self.is_air, self.is_sea]):
            raise ValidationError("At least one of Land, Air, or Sea must be selected.")


class PackageType(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=100, verbose_name="Package Name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    length = models.DecimalField(verbose_name="Length", decimal_places=2, max_digits=10)
    breadth = models.DecimalField(verbose_name="Breadth", decimal_places=2, max_digits=10)
    width = models.DecimalField(verbose_name="Width", decimal_places=2, max_digits=10)
    length_unit = models.ForeignKey(UnitofMeasurementLength, on_delete=models.CASCADE, related_name='package_length_unit')
    container_type = models.CharField(choices=[("LCL", "LCL"), ("FCL", "FCL")], max_length=5)
    active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    added_by = models.ForeignKey(User, blank=True, null=True, default=get_current_user, on_delete=models.PROTECT)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Package Type"

    def __str__(self):
        return self.name

    def clean(self):
        if self.length <= 0 or self.breadth <= 0 or self.width <= 0:
            raise ValidationError("Length, Breadth, and Width must all be greater than 0.")


def generate_custom_uuid():
    last_shipment = Branch.objects.all().order_by('-id').first()
    last_shipment_id = last_shipment.id if last_shipment else 0
    unique_number = last_shipment_id + 300

    return f"BRANCH-{unique_number:08d}"

class Branch(models.Model):
    BRANCH_STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('closed', 'Closed'),
        ('under_construction', 'Under Construction'),
    ]    
    branch_id = models.CharField(max_length=20, unique=True, verbose_name='Branch ID',blank=True,null=True,default=generate_custom_uuid)
    name = models.CharField(max_length=100, verbose_name='Branch Name')
    address = models.CharField(max_length=255, verbose_name='Address')
    city = models.CharField(max_length=100, verbose_name='City')
    state = models.CharField(max_length=100, verbose_name='State')
    postal_code = models.CharField(max_length=20, verbose_name='Postal Code')
    country = models.CharField(max_length=100, verbose_name='Country')
    contact_number = models.CharField(max_length=15, verbose_name='Contact Number')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    manager_name = models.CharField(max_length=100, verbose_name='Manager Name')
    manager_contact = models.CharField(max_length=15, verbose_name='Manager Contact')
    operational_hours = models.CharField(max_length=100, verbose_name='Operational Hours')
    status = models.CharField(max_length=20, choices=BRANCH_STATUS_CHOICES, default='operational', verbose_name='Status')
    established_date = models.DateField(verbose_name='Established Date', blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    incharges=models.ManyToManyField(User,related_name="company_branch_head",null=True,blank=True)
    added_by=models.ForeignKey(User,blank=True,null=True,default=get_current_user,on_delete=models.PROTECT)
    history = HistoricalRecords() 

    def __str__(self):
        return f"{self.name} ({self.branch_id})"

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['name']
        indexes = [
            models.Index(fields=['branch_id'], name='branch_id_idx'),
            models.Index(fields=['name'], name='branch_name_idx'),
        ]



MASTER_DATA_TYPE=[
    ("INCO","INCO"),
    ("STATUS","STATUS"),
    ("CONTAINER_TYPE","CONTAINER_TYPE"),
    ("CARGO_TYPE","CARGO_TYPE"),
    ("TRAILER_TYPE","TRAILER_TYPE"),
    ("DELIVERY_TYPE","DELIVERY_TYPE"),
    ("ShipmenSubType","ShipmenSubTyp"),
    ("INCO","INCO"),
]

class MasterData(models.Model):
    id=models.BigAutoField(primary_key=True)
    type_master=models.CharField(choices=MASTER_DATA_TYPE,max_length=100)
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    history = HistoricalRecords() 



class ApplicationSettings(models.Model):
    name = models.CharField(max_length=255, default='My Logistics Company')
    logo = models.ImageField(upload_to='logos/', default='logos/default_logo.png')
    country = models.CharField(max_length=100, default='United States')
    state = models.CharField(max_length=100, default='California', blank=True, null=True)
    address = models.TextField(default='123 Logistics Blvd, Suite 101, San Francisco, CA, 94101')
    bank_details = models.TextField(default='Bank: XYZ Bank, Account: 123456789, Branch: San Francisco')
    accounting_details = models.TextField(default='Account type: Checking, Financial period: January - December')
    financial_period_start = models.DateField(default='2025-01-01')
    financial_period_end = models.DateField(default='2025-12-31')
    phone = models.CharField(max_length=20, verbose_name="Phone", default='+1 800 555 1234')
    email = models.EmailField(blank=True, null=True, verbose_name="Email", default='info@logisticscompany.com')
    PAN = models.CharField(max_length=200, blank=True, null=True, verbose_name="PAN", default='ABCPQ1234D')



    def save(self, *args, **kwargs):
        if not self.pk and ApplicationSettings.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Singleton Setting"
        verbose_name_plural = "Singleton Settings"
 
class ShipmentPrefixes(models.Model):
    shipment_prefix = models.CharField(max_length=20, default='SHIP', blank=True, null=True)
    journal_voucher_prefix = models.CharField(max_length=20, default='JV', blank=True, null=True)
    cash_transfer_prefix = models.CharField(max_length=20, default='CT', blank=True, null=True)
    packages_prefix = models.CharField(max_length=20, default='PKG', blank=True, null=True)
    bill_prefix = models.CharField(max_length=20, default='BILL', blank=True, null=True)
    invoice_prefix = models.CharField(max_length=20, default='INV', blank=True, null=True)
    credit_note_prefix = models.CharField(max_length=20, default='CN', blank=True, null=True)
    cheque_prefix = models.CharField(max_length=20, default='CHQ', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and ShipmentPrefixes.objects.exists():
            raise ValidationError("Only one instance of this model is allowed.")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Shipment Prefixes"
        verbose_name_plural = "Shipment Prefixes"