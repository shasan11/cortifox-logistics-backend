from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import transaction, models
from decimal import Decimal
from .models import CashTransfers, JournalEntry, ChequeRegister, BankAccounts, Currency, JournalEntryItems, ChartofAccounts
from master.models import ShipmentPrefixes
import logging

logger = logging.getLogger(__name__)

# Fetch ShipmentPrefixes and ensure existence
try:
    main_data = ShipmentPrefixes.objects.first()
    if main_data:
        ct = main_data.cash_transfer_prefix
        jv = main_data.journal_voucher_prefix
    else:
        ct, jv = "CT", "JV"  # Defaults if ShipmentPrefixes is missing
except Exception as e:
    ct, jv = "CT", "JV"
    logger.error("Failed to fetch ShipmentPrefixes: %s", e)

# Signal for generating auto-incremented bill number for CashTransfers
@receiver(pre_save, sender=CashTransfers)
def generate_cash_transfer_bill_no(sender, instance, **kwargs):
    if not instance.bill_no:
        last_transfer = CashTransfers.objects.order_by('id').last()
        new_id = (last_transfer.id + 1) if last_transfer else 1
        instance.bill_no = f"{ct}-{new_id:04}"

# Signal for generating auto-incremented journal entry number for JournalEntry
@receiver(pre_save, sender=JournalEntry)
def generate_journal_entry_no(sender, instance, **kwargs):
    if not instance.journal_entry_no:
        last_entry = JournalEntry.objects.order_by('id').last()
        new_id = (last_entry.id + 1) if last_entry else 1
        instance.journal_entry_no = f"{jv}-{new_id:04}"

# Signal for updating BankAccount balances after ChequeRegister status changes
@receiver(post_save, sender=ChequeRegister)
def update_bank_account_balance(sender, instance, **kwargs):
    try:
        if instance.status == 'cleared' and instance.bank_account:
            account = instance.bank_account
            with transaction.atomic():
                if instance.cheque_type == 'issued':
                    account.opening_balance -= Decimal(instance.amount)
                elif instance.cheque_type == 'received':
                    account.opening_balance += Decimal(instance.amount)
                account.save()
    except Exception as e:
        logger.error("Failed to update bank account balance: %s", e)

# Signal to validate currency consistency before a cash transfer
@receiver(pre_save, sender=CashTransfers)
def validate_cash_transfer_currency(sender, instance, **kwargs):
    try:
        if instance.paid_from and instance.to_account:
            if instance.paid_from.currency != instance.to_account.currency:
                raise ValueError("Cash transfer accounts must have the same currency.")
    except ValueError as e:
        logger.error("Currency validation failed: %s", e)
        raise

# Signal for handling default currency enforcement
@receiver(pre_save, sender=Currency)
def enforce_single_default_currency(sender, instance, **kwargs):
    try:
        if instance.is_default:
            with transaction.atomic():
                Currency.objects.filter(is_default=True).exclude(pk=instance.pk).update(is_default=False)
    except Exception as e:
        logger.error("Failed to enforce single default currency: %s", e)

# Signal to update bank account balances after a cash transfer
@receiver(post_save, sender=CashTransfers)
def update_bank_balances_from_cash_transfer(sender, instance, **kwargs):
    try:
        if instance.paid_from and instance.to_account:
            with transaction.atomic():
                paid_from = BankAccounts.objects.select_for_update().get(pk=instance.paid_from.pk)
                to_account = BankAccounts.objects.select_for_update().get(pk=instance.to_account.pk)

                paid_from.opening_balance -= Decimal(instance.amount)
                paid_from.save()

                to_account.opening_balance += Decimal(instance.amount)
                to_account.save()
    except Exception as e:
        logger.error("Failed to update bank balances for cash transfer: %s", e)

# Signal to validate sufficient balance before issuing a cheque
@receiver(pre_save, sender=ChequeRegister)
def validate_cheque_balance(sender, instance, **kwargs):
    try:
        if instance.cheque_type == 'issued' and instance.bank_account:
            if instance.bank_account.opening_balance < Decimal(instance.amount):
                raise ValueError("Insufficient balance to issue this cheque.")
    except ValueError as e:
        logger.error("Cheque balance validation failed: %s", e)
        raise

# Helper function to update Chart of Accounts balance
def update_chart_of_accounts_balance(chart_of_accounts):
    try:
        total_debit = JournalEntryItems.objects.filter(chart_of_accounts=chart_of_accounts).aggregate(
            total_debit=models.Sum('dr_amount')
        )['total_debit'] or Decimal(0)

        total_credit = JournalEntryItems.objects.filter(chart_of_accounts=chart_of_accounts).aggregate(
            total_credit=models.Sum('cr_amount')
        )['total_credit'] or Decimal(0)

        chart_of_accounts.dr_amount = total_debit
        chart_of_accounts.cr_amount = total_credit
        chart_of_accounts.save()
    except Exception as e:
        logger.error("Failed to update Chart of Accounts balance: %s", e)

# Signal to update Chart of Accounts on JournalEntryItem creation or update
@receiver(post_save, sender=JournalEntryItems)
def update_coa_on_journal_item_save(sender, instance, **kwargs):
    update_chart_of_accounts_balance(instance.chart_of_accounts)

# Signal to update Chart of Accounts on JournalEntryItem deletion
@receiver(post_delete, sender=JournalEntryItems)
def update_coa_on_journal_item_delete(sender, instance, **kwargs):
    update_chart_of_accounts_balance(instance.chart_of_accounts)
