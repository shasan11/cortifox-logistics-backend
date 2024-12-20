import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.getCurrentUser import get_current_user
from accounting.models import ChartofAccounts
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords


class UnitofMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    desc = models.TextField(blank=True, null=True)
    accept_fraction = models.BooleanField(default=False)   
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='unit_of_measurement_added', default=get_current_user) 
    history = HistoricalRecords()
    

class ProductCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_product_category')
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_category_added', default=get_current_user)
    history = HistoricalRecords()

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=100, choices=(("Goods", "Goods"), ("Service", "Service")))
    code = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    hs_code = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sales_account = models.ForeignKey(ChartofAccounts, on_delete=models.CASCADE, related_name='sales_account_product')
    purchase_account = models.ForeignKey(ChartofAccounts, on_delete=models.CASCADE, related_name='purchase_account_product')
    sales_account_return = models.ForeignKey(ChartofAccounts, on_delete=models.CASCADE, related_name='sales_account_return_product')
    purchase_account_return = models.ForeignKey(ChartofAccounts, on_delete=models.CASCADE, related_name='purchase_account_return_product')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_added', default=get_current_user)
    stock = models.FloatField(default=0)
    history = HistoricalRecords()

class SecondaryUnit(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="sec_unit_product")
    conversion_rate = models.FloatField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_sec_unit_added', default=get_current_user)
     
class InventoryAdjustment(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="inventory_adjustment_product")
    date = models.DateField()
    reference = models.CharField(blank=True, null=True, max_length=30)
    quantity = models.FloatField(default=1, validators=[MinValueValidator(1)])
    stock_type = models.CharField(max_length=100, choices=(("In", "In"), ("Out", "Out")))
    rate = models.FloatField(default=1, validators=[MinValueValidator(1)])    
    desc_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_inventory_adjustment_added', default=get_current_user)

 
class BillofMaterials(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_of_good=models.CharField(choices=(("BOM","BOM"),("Production Order","Production Order"),("Production Journal","Production Journal")),max_length=100)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="bom_product")
    output=models.FloatField(blank=True,null=True)
    manufature_every_order=models.BooleanField(default=False)
    desc_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bom_added_by', default=get_current_user)
    history = HistoricalRecords()

class BillofMaterialRawMateials(models.Model):
    id = models.BigAutoField(primary_key=True)
    bom = models.ForeignKey(BillofMaterials, on_delete=models.PROTECT, related_name="bill_of_material")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="raw_material")
    output=models.FloatField()
    desc_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bom_raw_material_added', default=get_current_user)
    history = HistoricalRecords()

class BillofMaterialOutput(models.Model):
    id = models.BigAutoField(primary_key=True)
    bom = models.ForeignKey(BillofMaterials, on_delete=models.PROTECT, related_name="bill_of_material_output")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="by_product")
    output=models.FloatField(blank=True,null=True)
    percentage_of_cost=models.FloatField()
    desc_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bom_output_added', default=get_current_user)
    history = HistoricalRecords()

class BOMCosting(models.Model):
    id = models.BigAutoField(primary_key=True)
    bom = models.ForeignKey(BillofMaterials, on_delete=models.PROTECT, related_name="bill_of_material_costing")
    percentage_of_cost=models.DecimalField(decimal_places=2,max_digits=10)
    production_cost_terms = models.TextField(blank=True, null=True)
    desc_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bom_costing', default=get_current_user)
    history = HistoricalRecords()







    


    


