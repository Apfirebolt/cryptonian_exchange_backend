from django.urls import path
from . views import ListCustomUsersApiView, CreateCustomUserApiView, CustomTokenObtainPairView \
, RetrieveUpdateDestroyCustomUserApiView , ListCreateCurrencyApiView, RetrieveUpdateDestroyCurrencyApiView, ListCreateWalletApiView \
, RetrieveUpdateDestroyWalletApiView, ListCreateTransactionApiView, RetrieveUpdateDestroyTransactionApiView, ListCreateOrderApiView \
, RetrieveUpdateDestroyOrderApiView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register', CreateCustomUserApiView.as_view(), name='signup'),
    path('login', CustomTokenObtainPairView.as_view(), name='signin'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('users', ListCustomUsersApiView.as_view(), name='list-users'),
    path('users/<int:pk>', RetrieveUpdateDestroyCustomUserApiView.as_view(), name='user-detail'),
    path('currencies', ListCreateCurrencyApiView.as_view(), name='currencies'),
    path('currencies/<int:pk>', RetrieveUpdateDestroyCurrencyApiView.as_view(), name='currency-detail'),
    path('wallets', ListCreateWalletApiView.as_view(), name='wallets'),
    path('wallets/<str:pk>', RetrieveUpdateDestroyWalletApiView.as_view(), name='wallet-detail'),
    path('transactions', ListCreateTransactionApiView.as_view(), name='transactions'),
    path('transactions/<str:pk>', RetrieveUpdateDestroyTransactionApiView.as_view(), name='transaction-detail'),
    path('orders', ListCreateOrderApiView.as_view(), name='orders'),
    path('orders/<str:pk>', RetrieveUpdateDestroyOrderApiView.as_view(), name='order-detail'),
]