from django.db import models
from django.contrib.auth.models import User
from core.getCurrentUser import get_current_user
from simple_history.models import HistoricalRecords

class UnitofMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50, verbose_name="Unit Name")
    symbol = models.CharField(max_length=50, verbose_name="Unit Symbol")
    conversion_to_kg = models.DecimalField(verbose_name="Conversion to Kilogram", decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    add_by=models.ForeignKey(User,blank=True,null=True,default=get_current_user,on_delete=models.PROTECT,related_name="un_add")
    history = HistoricalRecords() 
   
    class Meta:
        verbose_name = "Unit of Measurement"

    def __str__(self):
        return self.name


class UnitofMeasurementLength(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50, verbose_name="Unit Name")
    symbol = models.CharField(max_length=50, verbose_name="Unit Symbol")
    conversion_to_cm = models.DecimalField(verbose_name="Conversion to Centi Meters", decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    added_by=models.ForeignKey(User,blank=True,null=True,default=get_current_user,on_delete=models.PROTECT,related_name="unl_add")
    history = HistoricalRecords() 
    
    class Meta:
        verbose_name = "Unit of Measurement (Length)"

    def __str__(self):
        return self.name


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
    added_by=models.ForeignKey(User,blank=True,null=True,default=get_current_user,on_delete=models.PROTECT)
    history = HistoricalRecords() 

    class Meta:
        verbose_name = "Ports"

    def __str__(self):
        return self.name


class PackageType(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=100, verbose_name="Package Name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    length = models.DecimalField(verbose_name="Length", decimal_places=2, max_digits=10)
    breadth = models.DecimalField(verbose_name="Breadth", decimal_places=2, max_digits=10)
    width = models.DecimalField(verbose_name="Width", decimal_places=2, max_digits=10)
    length_unit = models.ForeignKey(UnitofMeasurementLength, on_delete=models.CASCADE, related_name='package_length_unit')
    container_type=models.CharField(choices=[("LCL","LCL"),("FCL","FCL")],max_length=5)
    active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    added_by=models.ForeignKey(User,blank=True,null=True,default=get_current_user,on_delete=models.PROTECT)
    history = HistoricalRecords() 
    
    class Meta:
        verbose_name = "Package Type"

    def __str__(self):
        return self.name

class Branch(models.Model):
    BRANCH_STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('closed', 'Closed'),
        ('under_construction', 'Under Construction'),
    ]    
    branch_id = models.CharField(max_length=20, unique=True, verbose_name='Branch ID')
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
    incharges=models.ManyToManyField(User,related_name="company_branch_head")
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
    ("INCO","INCO"),
]

class MasterData(models.Model):
    id=models.BigAutoField(primary_key=True)
    type_master=models.CharField(choices=MASTER_DATA_TYPE,max_length=100)
    name=models.CharField(max_length=100)
    history = HistoricalRecords() 
 
 
 