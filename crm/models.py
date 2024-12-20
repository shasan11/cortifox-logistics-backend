from django.db import models
import uuid 
from django.contrib.auth.models import User
from core.getCurrentUser import get_current_user
from simple_history.models import HistoricalRecords


class ContactsGroup(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Name")
    under = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Under")
    description = models.TextField(blank=True, null=True, verbose_name="Description")    
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user)
    active=models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name or str(self.uuid)

    class Meta:
        verbose_name_plural = "Contact Groups"


class Contacts(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    contact_group = models.ForeignKey(ContactsGroup, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Contact Group")
    name = models.CharField(max_length=50, verbose_name="Name")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    PAN = models.CharField(max_length=20, blank=True, null=True, verbose_name="PAN")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    previous_credit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Previous Credit")
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Credit Limit")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user)
    active=models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name or str(self.uuid)

    class Meta:
        verbose_name_plural = "Contacts"



class Deal(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)    
    deals_stage=models.CharField(choices=[("Pending","Pending"),("Won","Won"),("Lost","Lost")],max_length=120)
    deal_contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, verbose_name="Deal Contact")
    
    # Other fields for Deal information
    title = models.CharField(max_length=100, verbose_name="Title")
    assign_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name="assigned_deals", verbose_name="Assign To")
    lead_source = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="lead_sources", verbose_name="Lead Source")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    expected_revenue = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Expected Revenue")
    expected_closing_date = models.DateField(verbose_name="Expected Closing Date")
    
    contact=models.ManyToManyField(Contacts,blank=True,null=True,related_name="contact_deals")

    # Tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user)
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.title} - {self.deal_contact}"

    class Meta:
        verbose_name_plural = "Deals"

class LeadsActivity(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="activities", verbose_name="Deal")
    activity_type = models.CharField(max_length=50, verbose_name="Activity Type")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date of Activity")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Performed By")
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user,related_name="leads_activity_user_add")
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.activity_type} - {self.deal.title}"

    class Meta:
        verbose_name_plural = "Leads Activities"


class LeadsDocs(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="documents", verbose_name="Deal")
    document_name = models.CharField(max_length=100, verbose_name="Document Name")
    document_file = models.FileField(upload_to="leads_docs/", verbose_name="Document File")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Uploaded By")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Upload Date")
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user,related_name="leads_docs_user_add")
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.document_name} - {self.deal.title}"

    class Meta:
        verbose_name_plural = "Leads Documents"
