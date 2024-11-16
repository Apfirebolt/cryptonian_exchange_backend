from django.test import TestCase
from users.models import CustomUser
from core.models import Order, Transaction, Wallet, Currency


class CurrencyTestCase(TestCase):
    
    def setUp(self):
        self.currency = Currency.objects.create(
            name='Bitcoin',
            symbol='BTC',
            code='BTC',
            is_crypto=True
        )

    def test_currency_creation(self):
        self.assertEqual(self.currency.name, 'Bitcoin')
        self.assertEqual(self.currency.symbol, 'BTC')
        self.assertEqual(self.currency.code, 'BTC')
        self.assertTrue(self.currency.is_crypto)


class WalletTestCase(TestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )

        self.currency = Currency.objects.create(
            name='Bitcoin',
            symbol='BTC',
            code='BTC',
            is_crypto=True
        )

        self.wallet = Wallet.objects.create(
            user=self.user,
            currency=self.currency,
            balance=0
        )

    def test_wallet_creation(self):
        self.assertEqual(self.wallet.user.email, 'testuser@example.com')
        self.assertEqual(self.wallet.currency.name, 'Bitcoin')
        self.assertEqual(self.wallet.balance, 0)


class OrderTestCase(TestCase):
        
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )

        self.currency = Currency.objects.create(
            name='Bitcoin',
            symbol='BTC',
            code='BTC',
            is_crypto=True
        )

        self.order = Order.objects.create(
            user=self.user,
            currency=self.currency,
            order_type='BUY',
            price=100,
            quantity=1,
            status='PENDING'
        )

    def test_order_creation(self):
        self.assertEqual(self.order.user.email, 'testuser@example.com')
        self.assertEqual(self.order.currency.name, 'Bitcoin')
        self.assertEqual(self.order.order_type, 'BUY')
        self.assertEqual(self.order.price, 100)
        self.assertEqual(self.order.quantity, 1)
        self.assertEqual(self.order.status, 'PENDING')


class TransactionTestCase(TestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )

        self.currency = Currency.objects.create(
            name='Bitcoin',
            symbol='BTC',
            code='BTC',
            is_crypto=True
        )

        self.wallet = Wallet.objects.create(
            user=self.user,
            currency=self.currency,
            balance=0
        )

        self.transaction = Transaction.objects.create(
            wallet=self.wallet,
            currency=self.currency,
            transaction_type='DEPOSIT',
            amount=100
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.wallet.user.email, 'testuser@example.com')
        self.assertEqual(self.transaction.currency.name, 'Bitcoin')
        self.assertEqual(self.transaction.transaction_type, 'DEPOSIT')
        self.assertEqual(self.transaction.amount, 100)
        
    

