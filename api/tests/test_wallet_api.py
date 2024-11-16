"""
Tests for the wallet API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Wallet, Currency
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from api.serializers import WalletSerializer

WALLET_URL = reverse('api:wallets')
WALLET_DETAIL_URL = reverse('api:wallet-detail', args=[1])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def create_currency(**params):
    """Create and return a new currency."""
    return Currency.objects.create(**params)

def detail_wallet_url(pk):
    """Create and return a wallet detail URL."""
    return reverse('api:wallet-detail', args=[pk])


class PublicWalletApiTests(TestCase):
    """Test the public features of the wallet API."""

    def setUp(self):
        self.client = APIClient()

    
    def test_wallet_retrieve_unauthorized(self):
        """Test that authentication is required for retrieving currencies."""
        res = self.client.get(WALLET_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateWalletApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123', username='Test Name', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)

    
    def test_retrieve_wallets(self):
        """Test retrieving a list of wallets."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        Wallet.objects.create(user=self.user, currency=currency, balance=1000)
        Wallet.objects.create(user=self.user, currency=currency, balance=2000)

        res = self.client.get(WALLET_URL)

        wallets = Wallet.objects.all().order_by('created_at')
        serializer = WalletSerializer(wallets, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    
    def test_delete_wallet(self):
        """Test deleting a wallet."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        wallet = Wallet.objects.create(user=self.user, currency=currency, balance=1000)

        res = self.client.delete(detail_wallet_url(wallet.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


    def test_update_wallet(self):
        """Test updating a wallet."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        wallet = Wallet.objects.create(user=self.user, currency=currency, balance=1000)

        payload = {'balance': 2000}
        res = self.client.patch(detail_wallet_url(wallet.id), payload)

        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, payload['balance'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    
    def test_wallet_already_exists(self):
        """Test that wallet already exists."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        Wallet.objects.create(user=self.user, currency=currency, balance=1000)

        payload = {'user': self.user, 'currency': currency, 'balance': 1000}
        res = self.client.post(WALLET_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_wallet_create(self):
        """Test creating a wallet."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        payload = {'user': self.user.id, 'currency': currency.id, 'balance': 1000}
        res = self.client.post(WALLET_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        

    def test_user_cannot_update_other_user_wallet(self):
        """Test that user cannot update other user wallet."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        user = create_user(email='another_user@example.com', password='test123', username='Another Name', is_staff=True, is_superuser=False)

        wallet = Wallet.objects.create(user=user, currency=currency, balance=1000)

        payload = {'balance': 2000}
        res = self.client.patch(detail_wallet_url(wallet.id), payload)

        wallet.refresh_from_db()
        self.assertNotEqual(wallet.balance, payload['balance'])
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        

    