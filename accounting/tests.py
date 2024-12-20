from django.test import TestCase
from .models import CashTransfers, JournalEntry, ChequeRegister, BankAccounts, Currency
from decimal import Decimal

class SignalsTestCase(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(name="USD", code="USD", is_default=True)
        self.bank_account_from = BankAccounts.objects.create(
            name="Bank A", 
            account_number="123456789", 
            opening_balance=Decimal('1000.00'), 
            currency=self.currency
        )
        self.bank_account_to = BankAccounts.objects.create(
            name="Bank B", 
            account_number="987654321", 
            opening_balance=Decimal('500.00'), 
            currency=self.currency
        )

    def test_cash_transfer_bill_no_generation(self):
        cash_transfer = CashTransfers.objects.create(
            amount=Decimal('100.00'),
            paid_from=self.bank_account_from,
            to_account=self.bank_account_to
        )
        self.assertTrue(cash_transfer.bill_no.startswith("CT-"))

    def test_journal_entry_bill_no_generation(self):
        journal_entry = JournalEntry.objects.create(description="Test Entry")
        self.assertTrue(journal_entry.bill_no.startswith("JE-"))

    def test_update_bank_account_balance_on_cheque_clearance(self):
        cheque = ChequeRegister.objects.create(
            amount=Decimal('200.00'),
            bank_account=self.bank_account_from,
            cheque_type='issued',
            status='cleared'
        )
        self.bank_account_from.refresh_from_db()
        self.assertEqual(self.bank_account_from.opening_balance, Decimal('800.00'))

    def test_cash_transfer_currency_validation(self):
        another_currency = Currency.objects.create(name="EUR", code="EUR")
        bank_account_in_eur = BankAccounts.objects.create(
            name="Bank C", 
            account_number="567890123", 
            opening_balance=Decimal('300.00'), 
            currency=another_currency
        )
        with self.assertRaises(ValueError):
            CashTransfers.objects.create(
                amount=Decimal('100.00'),
                paid_from=self.bank_account_from,
                to_account=bank_account_in_eur
            )

    def test_handle_default_currency(self):
        another_currency = Currency.objects.create(name="EUR", code="EUR", is_default=True)
        self.currency.refresh_from_db()
        another_currency.refresh_from_db()
        self.assertFalse(self.currency.is_default)
        self.assertTrue(another_currency.is_default)

    def test_update_bank_account_balances_from_cash_transfer(self):
        cash_transfer = CashTransfers.objects.create(
            amount=Decimal('100.00'),
            paid_from=self.bank_account_from,
            to_account=self.bank_account_to
        )
        self.bank_account_from.refresh_from_db()
        self.bank_account_to.refresh_from_db()
        self.assertEqual(self.bank_account_from.opening_balance, Decimal('900.00'))
        self.assertEqual(self.bank_account_to.opening_balance, Decimal('600.00'))

    def test_validate_paid_from_account_balance(self):
        with self.assertRaises(ValueError):
            CashTransfers.objects.create(
                amount=Decimal('1100.00'),
                paid_from=self.bank_account_from,
                to_account=self.bank_account_to
            )
