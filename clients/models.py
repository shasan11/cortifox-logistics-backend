from django.db import models
import uuid
import datetime
from django.contrib.auth.models import User
from core.getCurrentUser import get_current_user
from crm.models import Contacts
from accounting.models import Currency
from actor.models import Vendor
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class ClientType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    under = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_clients')
    desc = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=20, unique=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user)
    active=models.BooleanField(default=True)
    history = HistoricalRecords()

class Client(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]
    
    PAYMENT_TERMS = (
    ('CIA', 'Cash in Advance (CIA)'),
    ('COD', 'Cash on Delivery (COD)'),
    ('NET30', 'Net 30'),
    ('NET60', 'Net 60'),
    ('EOM', 'End of Month (EOM)'),
    ('MFI', 'Month Following Invoice (MFI)'),
    ('INSTALLMENT', 'Installment Terms'),
    ('DUE_UPON_RECEIPT', 'Due Upon Receipt'),
    ('PARTIAL_PAYMENT', 'Partial Payment'),
    ('2_10_NET_30', '2/10 Net 30'),
    ('L_C', 'Letter of Credit (L/C)'),
    ('CONSIGNMENT', 'Consignment'),
    ('BILL_OF_EXCHANGE', 'Bill of Exchange'),
    ('PROGRESS_PAYMENTS', 'Progress Payments'),
    )


    id = models.BigAutoField(primary_key=True)
    logo=models.ImageField(upload_to='client_logo',null=True,blank=True)
    clientGroup=models.ForeignKey(ClientType,on_delete=models.PROTECT,blank=True,null=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Name")
    type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, verbose_name="Type")
    contact_person = models.CharField(max_length=50, verbose_name="Contact Person")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    email=models.EmailField(max_length=100,verbose_name="Email Address")
    address1 = models.TextField(verbose_name="Address 1")
    address2 = models.TextField(blank=True, null=True, verbose_name="Address 2")
    province = models.CharField(max_length=50, verbose_name="Province")
    country = models.CharField(max_length=50, verbose_name="Country")
    updated=models.DateTimeField(auto_now=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user,verbose_name="added_by_client")
    active=models.BooleanField(default=True)
    contact=models.ManyToManyField(Contacts,blank=True)
    currency=models.ForeignKey(Currency,on_delete=models.PROTECT,blank=True,null=True)
    payment_terms=models.CharField(choices=PAYMENT_TERMS,max_length=100,default="CIA",blank=True,null=True)
    related_vendor=models.ManyToManyField(Vendor,blank=True)
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='client_user',blank=True,null=True)
    history = HistoricalRecords()
    

    def __str__(self):
        return self.name or str(self.uuid)

    class Meta:
        verbose_name_plural = "Clients"


class Ticket(models.Model):
  STATUS_CHOICES = (
    ('OPEN', 'Open'),
    ('PENDING', 'Pending'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
    ('CLOSED', 'Closed'),
  )

  PRIORITY_CHOICES = (
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH', 'High'),
    ('URGENT', 'Urgent'),
  )
  id = models.BigAutoField(primary_key=True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE)
  title = models.CharField(max_length=55)
  description = models.TextField()
  opened_date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
  priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
  assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)  # Assigned support agent (consider User model for authentication)
  history = HistoricalRecords()
  
  def __str__(self):
    return f"Ticket #{self.id} - {self.title}"

class TicketActivity(models.Model):
    ACTION_CHOICES = (
        ('STATUS_CHANGE', 'Status Change'),
        ('COMMENT', 'Comment'),
        ('ASSIGN_AGENT', 'Assign Agent'),
    )

    ticket = models.ForeignKey(Ticket, related_name='activities', on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description_client = models.TextField()  # Detailed activity description (like status change or comments)
    description_user = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # User who performed the action
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the action was logged
    history = HistoricalRecords()

    def __str__(self):
        return f"Activity on Ticket #{self.ticket.id} - {self.action} by {self.created_by}"

class ClientDocuments(models.Model):
  id = models.BigAutoField(primary_key=True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name="client_documents")
  document_name = models.CharField(max_length=50, verbose_name="Document Name")
  document_no = models.CharField(max_length=50, verbose_name="Document Id/Code", null=True, blank=True)
  file = models.FileField(upload_to='documents/%Y-%m-%d')
  description = models.TextField(blank=True, null=True)
  updated = models.DateTimeField(auto_now=True)
  user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user)
  active = models.BooleanField(default=True)
  history = HistoricalRecords()

class RelatedConsignee(models.Model):
  id = models.BigAutoField(primary_key=True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name="client_consignee")
  address = models.TextField(verbose_name="Address")
  consignor_name = models.CharField(max_length=50, verbose_name="Consignor Name")
  consigner_phone = models.CharField(max_length=10, verbose_name="Consigner Phone Number")
  consigner_email = models.EmailField(verbose_name="Consigner Email Address")
  remarks = models.TextField(blank=True, null=True)
  province = models.CharField(max_length=50, verbose_name="Province")
  country = models.CharField(max_length=50, verbose_name="Country")
  history = HistoricalRecords()
