from django.urls import path
from . views import ListCustomUsersApiView, CreateCustomUserApiView, CustomTokenObtainPairView \
, RetrieveUpdateDestroyCustomUserApiView , ListCreateCurrencyApiView, RetrieveUpdateDestroyCurrencyApiView
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
]