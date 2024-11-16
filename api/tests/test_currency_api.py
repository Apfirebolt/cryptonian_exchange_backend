"""
Tests for the currency API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Currency
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from api.serializers import CurrencySerializer


CURRENCY_URL = reverse('api:currencies')
CURRENCY_DETAIL_URL = reverse('api:currency-detail', args=[1])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def detail_currency_url(pk):
    """Create and return a currency detail URL."""
    return reverse('api:currency-detail', args=[pk])


class PublicCurrencyApiTests(TestCase):
    """Test the public features of the currency API."""

    def setUp(self):
        self.client = APIClient()

    
    def test_currency_retrieve_unauthorized(self):
        """Test that authentication is required for retrieving currencies."""
        res = self.client.get(CURRENCY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateGroupApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123', username='Test Name', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_retrieve_currencies(self):
        """Test retrieving a list of currencies."""
        Currency.objects.create(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        Currency.objects.create(name='Bitcoin', symbol='BTC', code='BTC', is_crypto=True)

        res = self.client.get(CURRENCY_URL)

        currencies = Currency.objects.all().order_by('name')
        serializer = CurrencySerializer(currencies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_currency(self):
        """Test deleting a currency."""
        currency = Currency.objects.create(name='US Dollar', symbol='$', code='USD', is_crypto=False)

        res = self.client.delete(detail_currency_url(currency.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_currency(self):
        """Test updating a currency."""
        currency = Currency.objects.create(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        payload = {'name': 'US Dollar', 'symbol': '$', 'code': 'USD', 'is_crypto': True}

        res = self.client.patch(detail_currency_url(currency.id), payload)

        currency.refresh_from_db()

        self.assertEqual(currency.is_crypto, payload['is_crypto'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['is_crypto'], payload['is_crypto'])

    def test_currency_name_already_exists(self):
        """Test that currency name already exists."""
        Currency.objects.create(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        payload = {'name': 'US Dollar', 'symbol': '$', 'code': 'USD', 'is_crypto': True}

        res = self.client.post(CURRENCY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Currency already exists')