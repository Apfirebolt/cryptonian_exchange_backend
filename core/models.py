from django.db import models
from cryptonian_exchange_backend.settings import AUTH_USER_MODEL
from uuid import uuid4


class Currency(models.Model):
    name = models.CharField("Currency Name", max_length=255)
    symbol = models.CharField("Currency Symbol", max_length=10)
    code = models.CharField("Currency Code", max_length=10)
    is_crypto = models.BooleanField("Is Crypto", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Currency"
        verbose_name = "Currency"


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    balance = models.DecimalField("Balance", max_digits=20, decimal_places=10)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.currency.name}"

    class Meta:
        verbose_name_plural = "Wallet"
        verbose_name = "Wallet"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    order_type = models.CharField("Order Type", max_length=10)
    price = models.DecimalField("Price", max_digits=20, decimal_places=10)
    quantity = models.DecimalField("Quantity", max_digits=20, decimal_places=10)
    status = models.CharField("Status", max_length=10)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.currency.name}"

    class Meta:
        verbose_name_plural = "Order"
        verbose_name = "Order"


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    transaction_type = models.CharField("Transaction Type", max_length=10)
    amount = models.DecimalField("Amount", max_digits=20, decimal_places=10)
    created_at = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.email} - {self.currency.name}"

    class Meta:
        verbose_name_plural = "Transaction"
        verbose_name = "Transaction"