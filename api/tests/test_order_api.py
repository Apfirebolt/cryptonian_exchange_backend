"""
Tests for the transaction API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Order, Currency
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from api.serializers import OrderSerializer

ORDER_URL = reverse('api:orders')
ORDER_DETAIL_URL = reverse('api:order-detail', args=[1])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def create_currency(**params):
    """Create and return a new currency."""
    return Currency.objects.create(**params)

def detail_order_url(pk):
    """Create and return a order detail URL."""
    return reverse('api:order-detail', args=[pk])


class PublicOrderApiTests(TestCase):
    """Test the public features of the transaction API."""

    def setUp(self):
        self.client = APIClient()

    
    def test_transaction_retrieve_unauthorized(self):
        """Test that authentication is required for retrieving currencies."""
        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateTransactionApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123', username='Test Name', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_create_order(self):
        """Test creating a new order."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        payload = {
            'user': self.user.id,
            'currency': currency.id,
            'order_type': 'buy',
            'price': 100,
            'quantity': 10,
            'status': 'pending'
        }
        res = self.client.post(ORDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        
    def test_retrieve_orders(self):
        """Test retrieving a list of orders."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        Order.objects.create(user=self.user, currency=currency, order_type='buy', price=100, quantity=10, status='pending')
        Order.objects.create(user=self.user, currency=currency, order_type='sell', price=200, quantity=20, status='completed')

        res = self.client.get(ORDER_URL)

        orders = Order.objects.all().order_by('created_at')
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    
    def test_delete_order(self):
        """Test deleting a order."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        order = Order.objects.create(user=self.user, currency=currency, order_type='buy', price=100, quantity=10, status='pending')

        res = self.client.delete(detail_order_url(order.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_order(self):
        """Test updating a order."""
        currency = create_currency(name='US Dollar', symbol='$', code='USD', is_crypto=False)
        order = Order.objects.create(user=self.user, currency=currency, order_type='buy', price=100, quantity=10, status='pending')

        payload = {'quantity': 20}
        res = self.client.patch(detail_order_url(order.id), payload)

        order.refresh_from_db()
        self.assertEqual(order.quantity, payload['quantity'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    
    