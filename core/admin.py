from django.contrib import admin
from core.models import Order, Transaction, Wallet, Currency


admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(Currency)

