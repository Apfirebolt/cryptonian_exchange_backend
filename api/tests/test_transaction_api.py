"""
Tests for the transaction API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Transaction, Currency, Wallet
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from api.serializers import TransactionSerializer

TRANSACTION_URL = reverse('api:transactions')
TRANSACTION_DETAIL_URL = reverse('api:transaction-detail', args=[1])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def create_currency(**params):
    """Create and return a new currency."""
    return Currency.objects.create(**params)

def create_wallet(**params):
    """Create and return a new wallet."""
    return Wallet.objects.create(**params)

def detail_TRANSACTION_url(pk):
    """Create and return a transaction detail URL."""
    return reverse('api:transaction-detail', args=[pk])

# class Transaction(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
#     currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
#     transaction_type = models.CharField("Transaction Type", max_length=10)
#     amount = models.DecimalField("Amount", max_digits=20, decimal_places=10)
#     created_at = models.DateTimeField("Created At", auto_now_add=True)


class PublicTransactionApiTests(TestCase):
    """Test the public features of the transaction API."""

    def setUp(self):
        self.client = APIClient()

    
    def test_transaction_retrieve_unauthorized(self):
        """Test that authentication is required for retrieving currencies."""
        res = self.client.get(TRANSACTION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateTransactionApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123', username='Test Name', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)

    
    def test_retrieve_transactions(self):
        """Test retrieving a list of transactions."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        wallet = create_wallet(user=self.user, currency=currency, balance=1000)
        Transaction.objects.create(wallet=wallet, currency=currency, transaction_type='deposit', amount=1000)
        Transaction.objects.create(wallet=wallet, currency=currency, transaction_type='withdraw', amount=500)

        res = self.client.get(TRANSACTION_URL)

        transactions = Transaction.objects.all().order_by('created_at')
        serializer = TransactionSerializer(transactions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

    def test_delete_transaction(self):
        """Test deleting a transaction."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        wallet = create_wallet(user=self.user, currency=currency, balance=1000)
        transaction = Transaction.objects.create(wallet=wallet, currency=currency, transaction_type='deposit', amount=1000)

        res = self.client.delete(detail_TRANSACTION_url(transaction.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


    def test_update_transaction(self):
        """Test updating a transaction."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        wallet = create_wallet(user=self.user, currency=currency, balance=1000)
        transaction = Transaction.objects.create(wallet=wallet, currency=currency, transaction_type='deposit', amount=1000)

        payload = {'amount': 2000}
        res = self.client.patch(detail_TRANSACTION_url(transaction.id), payload)

        transaction.refresh_from_db()
        self.assertEqual(transaction.amount, payload['amount'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_retrieve_transaction(self):
        """Test retrieving a transaction."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        wallet = create_wallet(user=self.user, currency=currency, balance=1000)
        transaction = Transaction.objects.create(wallet=wallet, currency=currency, transaction_type='deposit', amount=1000)

        res = self.client.get(detail_TRANSACTION_url(transaction.id))

        serializer = TransactionSerializer(transaction)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    