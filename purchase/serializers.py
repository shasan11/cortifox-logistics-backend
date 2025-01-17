from rest_framework import serializers
from .models import (
    ExpenseCategory,
    Expenses,
    ExpensesItems,
    VendorBills,
    VendorBillItems,
    VendorPayments,
    VendorPaymentEntries,
)

from rest_framework_bulk.serializers import BulkSerializerMixin
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = "__all__"
        list_serializer_class = AdaptedBulkListSerializer



class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer



class ExpensesItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensesItems
        fields = [
            'id', 'expensesitems', 'description', 'amount', 'vat_choices',
        ]
        list_serializer_class = AdaptedBulkListSerializer



class VendorBillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorBills
        fields = [
            'id', 'vendor', 'invoice_reference', 'date', 'due_date', 'currency',
            'exchage_rate_to_npr', 'subtotal_amount', 'non_taxable_amount',
            'taxable_amount', 'discount_amount', 'vat_amount', 'total_amount',
            'paid_amount', 'remaining_amount', 'bill_status', 'remarks',
        ]
        list_serializer_class = AdaptedBulkListSerializer



class VendorBillItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorBillItems
        fields = [
            'id', 'vendorbills', 'description', 'rate', 'qty', 'taxes',
            'discount', 'vat_choices', 'total', 'remarks',
        ]
        list_serializer_class = AdaptedBulkListSerializer



class VendorPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPayments
        fields = [
            'id', 'paid_from', 'paid_to', 'date', 'remarks', 'due_date', 'currency',
            'exchage_rate_to_npr', 'amount', 'bank_charges', 'tds_amount',
            'tds_type', 'tds_coa', 'created', 'updated_date', 'user', 'bill_status',
        ]
        list_serializer_class = AdaptedBulkListSerializer



class VendorPaymentEntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPaymentEntries
        fields = [
            'id', 'vendor_payments', 'vendor_bills', 'amount',
        ]
        list_serializer_class = AdaptedBulkListSerializer

